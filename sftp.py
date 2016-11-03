import paramiko
from ctypes import c_char_p


def sftp(c_storage,client_details,server_details,download_paths,upload_paths):
    try:
        host = server_details.host
        port = 22
        transport = paramiko.Transport((host, port))

        password = server_details.password
        username = server_details.user
        transport.connect(username = username, password = password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        localpath = client_details.localpath
        for path in download_paths:
            sftp.get(localpath, path)
        for path in upload_paths:
            sftp.put(localpath, path)

        sftp.close()
        transport.close()
        c_storage.value = "Success"
    except:
        c_storage.value = "Failed"