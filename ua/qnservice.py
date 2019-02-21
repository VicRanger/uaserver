AK = 'e_h_B5nFMu1Uv7ZEXQV1WQfPupJWGX9O1SDrKcK0'
SK = '4J5p3CjmN_p5ikPL3YTCxQe-ODtgjzDwdeuVI8Dv'
BUCKET = 'uartisan'

from qiniu import Auth, put_file, etag
import qiniu.config

def uploadImg(fileUrl,fileName):
    q = Auth(AK, SK)
    token = q.upload_token(BUCKET, fileName, 3600)
    localFile = fileUrl
    ret,info = put_file(token, fileName, localFile)
    print(ret)