import logging

from apiclient import errors
from apiclient.http import MediaFileUpload
from oauth2client.client import Credentials

from wevolve.libs.drive_auth import build_service, GetCredentialsException, get_authorization_url


def connect_project_to_drive(request, project_part, userproject, drive_token):
    if not userproject.drive_auth and request.user.is_authenticated():
        drive_util = DriveUtil(drive_token, userproject.user.email)

        if not project_part.drive_id:
            drive_util.get_project_part_folder(request.user.profile.drive_folder,
                                               project_part)
        else:
            drive_util_created = DriveUtil(userproject.project.created_user.profile.drive_token)
            drive_util_created.insert_permission(project_part.project.drive_id,
                                                 request.user.email,
                                                 'user',
                                                 'writer'
                                                 )
            drive_util.insert_file_into_folder(request.user.profile.drive_folder,
                                               project_part.project.drive_id)
        userproject.drive_auth = True
        userproject.save()


def update_drive_folder(old_obj, new_title, user):
    drive_util = DriveUtil(user.profile.drive_token)
    foldername = '-'.join([str(old_obj.id), new_title])
    result = drive_util.rename_file_or_folder(old_obj.drive_id,
                                              foldername)
    return bool(result)


class DriveUtil():
    def __init__(self, credentials, user_email=None):
        if credentials:
            self.service = build_service(Credentials.new_from_json(credentials))
        else:
            logging.error('This user failed in credentials error %s and email %s' % (credentials, user_email))
            auth_url = 'no_url'
            if user_email:
                auth_url = get_authorization_url(user_email, 1)
            raise GetCredentialsException(auth_url)

    def get_file(self, file_id):
        """Print a file's metadata.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to print metadata for.
        """
        try:
            file = self.service.files().get(fileId=file_id).execute()
            return file
        except errors.HttpError, error:
            if error.resp.status == 401:
                self.redirect_auth()

    def rename_file_or_folder(self, file_id, new_title):
        try:
            f = {'title': new_title}

            updated_file = self.service.files().patch(fileId=file_id, body=f,
                                                      fields='title').execute()
            return updated_file
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None

    def delete_file(self, file_id):
        try:
            file = self.service.files().delete(fileId=file_id).execute()
            return file
        except errors.HttpError, error:
            if error.resp.status == 401:
                self.redirect_auth()

    def get_files(self, query=None):
        try:
            if query:
                files = self.service.files().list(q=query).execute()
            else:
                files = self.service.files().list().execute()
            return files
        except errors.HttpError, error:
            if error.resp.status == 401:
                self.redirect_auth()

    def get_files_in_folder(self, folder_id):
        """Get files belonging to a folder.

        Args:
          service: Drive API service instance.
          folder_id: ID of the folder to print files from.
        """
        page_token = None
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                children = self.service.children().list(
                    folderId=folder_id, **param).execute()

                for child in children.get('items', []):
                    pass
                page_token = children.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break

    def insert_folder(self, foldername, parent_id=None):
        body = {'title': foldername,
                'mimeType': 'application/vnd.google-apps.folder'
                }

        if parent_id:
            body['parents'] = [{'id': parent_id}]

        try:
            file = self.service.files().insert(body=body).execute()
            return file
        except errors.HttpError, error:
            print 'An error occured: %s' % error
            return None

    def insert_drive_file(self, filename, type_file, parent_id=None):
        FILES_AVAILABLE = ('document', 'presentation', 'spreadsheet',
                           'drawing', 'form')

        if type_file not in FILES_AVAILABLE:
            return None

        body = {'title': filename,
                'mimeType': 'application/vnd.google-apps.%s' % type_file
                }

        if parent_id:
            body['parents'] = [{'id': parent_id}]

        try:
            file = self.service.files().insert(body=body).execute()
            return file
        except errors.HttpError, error:
            print 'An error occured: %s' % error
            return None

    def insert_file(self, title, description, parent_id, mime_type, filename,
                    public=False):
        """Insert new file.

        Args:
          service: Drive API service instance.
          title: Title of the file to insert, including the extension.
          description: Description of the file to insert.
          parent_id: Parent folder's ID.
          mime_type: MIME type of the file to insert.
          filename: Filename of the file to insert.
        Returns:
          Inserted file metadata if successful, None otherwise.
        """
        media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=False)
        body = {
          'title': title,
          'description': description,
          'mimeType': mime_type
        }
        # Set the parent folder.
        if parent_id:
            body['parents'] = [{'id': parent_id}]

        try:
            file_obj = self.service.files().insert(body=body,
                                               media_body=media_body).execute()
            if public:
                # We decided anyone could access with the link of the file
                self.insert_permission(file_obj['id'], 'anyone', 'anyone', 'reader')

            return file_obj
        except errors.HttpError, error:
            print 'An error occured: %s' % error
            return None

    def get_or_create_folder(self, foldername, parent_id, public=False):
        folders = self.service.children().list(folderId=parent_id).execute()
        for folder in folders.get('items', []):
            f = self.get_file(folder['id'])
            if f and 'title' in f:
                if f['title'] == foldername:
                    return folder['id']
        folder = self.insert_folder(foldername, parent_id)
        if public:
            self.insert_permission(folder['id'], 'anyone', 'anyone', 'reader')
        try:
            return folder['id']
        except TypeError:
            return None

    def get_project_folder(self, parent_id, project):
        foldername = '-'.join([str(project.id), project.title])

        project_folder = self.get_or_create_folder(foldername, parent_id,
                                                   project.is_open())
        project.drive_id = project_folder
        project.save()
        return project_folder

    def get_project_part_folder(self, main_folder_id, project_part):
        project_folder = self.get_project_folder(main_folder_id,
                                                 project_part.project)
        foldername = '-'.join([str(project_part.id),
                               project_part.title])
        folders = self.service.children().list(folderId=project_folder).execute()

        project_part_folder = self.get_or_create_folder(foldername,
                                                        project_folder,
                                                        project_part.project.is_open())
        project_part.drive_id = project_part_folder
        project_part.save()
        return project_part_folder

    def insert_permission(self, file_id, value, perm_type, role):
        """Insert a new permission.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to insert permission for.
          value: User or group e-mail address, domain name or None for 'default'
               type.
          perm_type: The value 'user', 'group', 'domain' or 'default'.
          role: The value 'owner', 'writer' or 'reader'.
        Returns:
          The inserted permission if successful, None otherwise.
        """
        new_permission = {
            'value': value,
            'type': perm_type,
            'role': role
        }
        try:
            perms = self.service.permissions().insert(fileId=file_id,
                                                      body=new_permission).execute()
            return perms
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            print error.content
        return None

    def remove_permission(self, file_id, permission_id):
        """Remove a permission.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to remove the permission for.
          permission_id: ID of the permission to remove.
        """
        try:
            self.service.permissions().delete(fileId=file_id,
                                              permissionId=permission_id).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

    def remove_file_from_folder(self, folder_id, file_id):
        """Remove a file from a folder.

        Args:
          folder_id: ID of the folder to remove the file from.
          file_id: ID of the file to remove from the folder.
        """
        try:
            self.service.parents().delete(fileId=file_id, parentId=folder_id).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

    def insert_file_into_folder(self, folder_id, file_id):
        """Insert a file into a folder.

        Args:
          folder_id: ID of the folder to insert the file into.
          file_id: ID of the file to insert.
        Returns:
          The inserted parent if successful, None otherwise.
        """
        new_parent = {'id': folder_id}
        try:
            return self.service.parents().insert(fileId=file_id, body=new_parent).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None
