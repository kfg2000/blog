from django.http import JsonResponse
from allauth.socialaccount.admin import SocialApp
from requests_oauthlib import OAuth1
from urllib.parse import quote
import requests

def test(request):
	user = request.user
	social_account = user.socialaccount_set.get(user=user.id)

	token = social_account.socialtoken_set.get(account=social_account.id).token
	token_secret = social_account.socialtoken_set.get(account=social_account.id).token_secret

	social_app = SocialApp.objects.get(provider=social_account.provider)
	client_id = social_app.client_id
	secret = social_app.secret

	auth = OAuth1(client_id,secret,token,token_secret)

	query = quote("#django")
	url = "https://api.twitter.com/1.1/search/tweets.json?q="+query

	response = requests.get(url, auth=auth)
	return JsonResponse(response.json(),safe=False)