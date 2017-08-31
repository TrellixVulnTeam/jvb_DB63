from django.shortcuts import render  # noqa
from django.http import Http404
from django.http import HttpResponse
from rauth import OAuth1Service
import webbrowser 
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .serializers import GarminTokenSerializer
from .models import GarminToken
# In state=1 the next request should include an oauth_token.
#If it doesn't go back to 0

from django.views.decorators.clickjacking import xframe_options_exempt
import urllib
import logging
import requests
import time
import re
from utils.OAuthSimple import OAuthSimple


try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

def request_token(request):
    req_url = 'http://connectapi.garmin.com/oauth-service-1.0/oauth/request_token'
    authurl = 'http://connect.garmin.com/oauthConfirm'
    acc_url = 'http://connectapi.garmin.com/oauth-service-1.0/oauth/access_token'
    conskey = '6c1a770b-60b9-4d7e-83a2-3726080f5556';
    conssec = '9Mic4bUkfqFRKNYfM3Sy6i0Ovc9Pu2G4ws9';
    session = request.session
    if not 'auth_token' in session and ('state' in session and session['state'])==1:
        session['state'] = 0; 
    # try:


    service = OAuth1Service(
          # name = 'etrade',
          consumer_key = conskey,
          consumer_secret = conssec,
          request_token_url = req_url,
          access_token_url = acc_url,
          authorize_url = authurl, 
          # base_url = 'http://etws.etrade.com'
          )

    # Get request token and secret    
    # $oauth = new OAuth($conskey,$conssec,OAUTH_SIG_METHOD_HMACSHA1,OAUTH_AUTH_TYPE_URI)
    # $oauth->enableDebug()

    session = request.session
    request_token, request_token_secret = service.get_request_token()  

    # $request_token_info = $oauth->getRequestToken($req_url)
    session['request_token'] = request_token
    session['request_token_secret'] = request_token_secret
    session['state'] = 1
    callback_string = urllib.parse.quote('http://app.jvbwellness.com/callbacks/garmin')
    return redirect(authurl + '?oauth_token={0}&oauth_callback={1}'.format(request_token,callback_string))
    

  #   if not 'oauth_token' in session and not 'state' in session:
  #       # request_token, request_token_secret = service.get_request_token(params = 
  # #                     {'oauth_callback': 'oob', 
  # #                      'format': 'json'})

        # request_token, request_token_secret = service.get_request_token()               
        # # $request_token_info = $oauth->getRequestToken($req_url)
        # session['request_token'] = request_token
        # session['request_token_secret'] = request_token_secret
        # session['state'] = 1
        # return redirect(authurl + '?oauth_token={0}'.format(request_token))
  #   elif 'state' in session and session['state'] ==1:
  #       #oauth token already exists
  #       #determine access token temporaily for work  
  #       #continue
  #       access_token, access_token_secret = service.get_access_token(session['request_token'],
  #           session['request_token_secret'])

  #       # need to validate that the token still works.... not done
  #       session['state'] = 2
  #       session['access_token'] = access_token
  #       session['access_secret'] = access_token_secret
  #       return redirect('/')
    # except Exception, e:
    #     print(e)
    
def receive_token(request):
    req_url = 'http://connectapi.garmin.com/oauth-service-1.0/oauth/request_token'
    authurl = 'http://connect.garmin.com/oauthConfirm'
    acc_url = 'http://connectapi.garmin.com/oauth-service-1.0/oauth/access_token'
    conskey = '6c1a770b-60b9-4d7e-83a2-3726080f5556';
    conssec = '9Mic4bUkfqFRKNYfM3Sy6i0Ovc9Pu2G4ws9';
    session = request.session

    # oauth_token = request.GET['oauth_token'] 
    oauth_verifier = request.GET['oauth_verifier']

    # encoded_verifier = urllib.parse.quote(oauth_verifier)
    # xacc_url = '{0}?oauth_verifier={1}'.format(acc_url,encoded_verifier)    

    # oauth = OAuthSimple(apiKey=conskey, sharedSecret=conssec)
    # request = oauth.sign({
    #   'action': "POST",
    #   'path': acc_url,
    #   'parameters': {  'oauth_verifier': oauth_verifier,
    #     'oauth_token': oauth_token,
    #     'oauth_version': '1.0',
    #     'oauth_timestamp': time.time(),
    #   }
    # })

    # from requests_oauthlib import OAuth1, OAuth1Session
    # s = requests.Session()
    # auth = OAuth1(conskey, conssec, verifier=oauth_verifier, resource_owner_key=oauth_token)
    # s.auth = auth
    # s.headers.update({
    #     #'oauth_verifier': oauth_verifier,
    #     # 'oauth_token': oauth_token,
    #     'Content-Length': '0'
    #      })

    # print(s.headers)

    # print(request)
 

    # r = s.post(acc_url)
    # print(r.text)
    # print(r.json())

    service = OAuth1Service(
          # name = 'etrade',
          consumer_key = conskey,
          consumer_secret = conssec,
          request_token_url = req_url,
          access_token_url = acc_url,
          authorize_url = authurl, 
          # base_url = 'http://etws.etrade.com'
          )

    # #oauth_token=d37f1145-59b1-4f85-bc18-9a25e5697445&oauth_verifier=d9lZlU521B

    # print('oauth_token_secret')
    access_token, access_token_secret = service.get_access_token(session['request_token'],
    session['request_token_secret'],method='POST',data={'oauth_verifier': oauth_verifier},
    header_auth=True)

    # sess = service.get_auth_session(session['request_token'], session['request_token_secret'],method='POST',data={'oauth_verifier': oauth_verifier}, header_auth=True)
    sess = service.get_session((access_token, access_token_secret))

    # # need to validate that the token still works.... not done
    # session['state'] = 2
    # session['access_token'] = access_token
    # session['access_secret'] = access_token_secret
    # print('access token')
    # print(access_token)
    # print('access_token_secret')
    # print(access_token_secret)
    # session = service.get_auth_session(access_token,access_token_secret,method='POST',data=data)
    


    # data = {
    #   'uploadStartTimeInSeconds': 1503148183-86300,
    #   'uploadEndTimeInSeconds': 1503148183,
    # }
    
    # count = 0 
    # while count < 20:
    #     r = sess.get('https://healthapi.garmin.com/wellness-api/rest/epochs', header_auth=True, params=data)
    #     print(r)
    #     print(r.json())        
    #     count += 1
    #     data['uploadEndTimeInSeconds'] = data['uploadStartTimeInSeconds']
    #     data['uploadStartTimeInSeconds'] = data['uploadStartTimeInSeconds'] - 86300

    # session.headers.update({'access-token': access_token})
    # print(r.json())

    # from requests_oauthlib import OAuth1, OAuth1Session
    # s = requests.Session()
    # auth = OAuth1(conskey, conssec, resource_owner_key=access_token)
    # s.auth = auth
    # s.headers.update({
    #     #'oauth_verifier': oauth_verifier,
    #     # 'oauth_token': oauth_token,
    #     'Content-Length': '0'
    #      })


    # print(s.headers)

    # print(request)
    
    request.session['token'] = access_token
    request.session['token_secret'] = access_token_secret
    request.session['oauth_verifier'] = oauth_verifier

    # print("\n\nACCESS TOKEN:", access_token)
    # print("\n\nACCES TOKEN SECRET:", access_token_secret)

    # data = {'token':access_token, 'secret':access_token_secret}
    # url = "/garmin_token/"
    # requests.post(url,data=data)

    return redirect('/service_connect')

    
    # print(request)
    # $json = json_decode($_POST['uploadMetaData']);
    # $tmp_name = $_FILES['file']['tmp_name'];
    # $file_name = $_FILES['file']['name']; 
    # move_uploaded_file($tmp_name, YOUR_FILE_PATH); 
    # header('Location: YOUR_URL_FOR_THE_SAVED_FILE', true, 201);


# class GetGarminToken(APIView):
#   permission_classes = (permissions.IsAuthenticated,)
#   def dispatch(self, *args, **kwargs):
#     try:
#       if GarminToken.objects.get(user=self.request.user):
#         return super(GetGarminToken,self).dispatch(*args,**kwargs)
#     except GarminToken.DoesNotExist:
#       return redirect('/users/request_token')
#     return redirect('/users/request_token')

#   def get_object(self,user):
#     return GarminToken.objects.get(user=user)
#     # request_token(self.request)
#     redirect('/users/request_token')
#     return GarminToken.objects.get(user=user)
#     pass

#   def get(self, request, format="json"):
#       token = self.get_object(user=request.user)
#       token = self.request.session['token']
#       serializers = GarminTokenSerializer(token)
#       return Response(serializers.data)
#       return Response({'token':token})

#   def post(self, request, format="json"):
#     serializer = GarminTokenSerializer(data=request.data,context={'request': request})
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data,status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class fetchGarminData(APIView):

  def get(self, request, format="json"):
    req_url = 'http://connectapi.garmin.com/oauth-service-1.0/oauth/request_token'
    authurl = 'http://connect.garmin.com/oauthConfirm'
    acc_url = 'http://connectapi.garmin.com/oauth-service-1.0/oauth/access_token'
    conskey = '6c1a770b-60b9-4d7e-83a2-3726080f5556';
    conssec = '9Mic4bUkfqFRKNYfM3Sy6i0Ovc9Pu2G4ws9';
    session = request.session

    access_token = session.get('token',None)
    access_token_secret = session.get('token_secret',None)

    if access_token and access_token_secret:
      service = OAuth1Service(
            consumer_key = conskey,
            consumer_secret = conssec,
            request_token_url = req_url,
            access_token_url = acc_url,
            authorize_url = authurl, 
            )
      sess = service.get_session((access_token, access_token_secret))
      data = {
        'uploadStartTimeInSeconds': 1503187200-86300,
        'uploadEndTimeInSeconds': 1503187200,
      }
      
      r = sess.get('https://healthapi.garmin.com/wellness-api/rest/epochs', header_auth=True, params=data)
      return Response(r.json)
    else:
      return Response(status.HTTP_401_UNAUTHORIZED)