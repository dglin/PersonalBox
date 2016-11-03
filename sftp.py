import paramiko
from ctypes import c_char_p


def sftp(serverAddress, serverPath, localPath, username, password, sftp_list):
    try:
        host = serverAddress
        port = 22
        transport = paramiko.Transport((host, port))

        password = password
        username = username
        transport.connect(username = username, password = password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        for path in sftp_list:
            print localPath + path
            sftp.put(localPath + path, serverPath)

        sftp.close()
        transport.close()
        return "Success"
    except Exception as e:
        return e