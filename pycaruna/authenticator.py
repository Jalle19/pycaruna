from urllib.parse import urlparse, parse_qs
import requests
import pycaruna.utils as utils
from bs4 import BeautifulSoup


class Authenticator:
    def __init__(self, username, password):
        """
        :param username: your e-mail address
        :param password: your password
        """
        self.username = username
        self.password = password
        pass

    def login(self):
        """
        Performs the login dance required to obtain cookies etc. for further API communication
        """
        s = requests.session()

        # Start the authentication flow. This page will do some redirects and finally return a JSON object containing
        # a URL we have to visit manually
        r = s.post(utils.create_caruna_plus_url('/authorization/login'), json={
            'language': 'fi',
            'redirectAfterLogin': 'https://plus.caruna.fi/',
        })

        r = s.get(r.json()['loginRedirectUrl'])

        # Parse the <meta http-equiv="refresh"> URL and request it (ng2Postresponder)
        url = BeautifulSoup(r.content, 'lxml').findAll('meta')[0]['content'][6:]
        r = s.get("https://authentication2.caruna.fi" + url)

        # Now we're at the actual login page. We need to find the <form>, get its "action" attribute, then modify it
        # so it actually posts to the correct place. Normally the form submission and action mangling is done by
        # JavaScript.
        c = r.content
        soup = BeautifulSoup(c, 'lxml')
        action = "/login?2-1.0-userIDPanel-usernameLogin-loginWithUserID"

        # Build form variables (all hidden variables must always be included)
        svars = utils.get_hidden_form_vars(soup)
        svars['ttqusername'] = self.username
        svars['userPassword'] = self.password
        svars[soup.find('input', type="submit")['name']] = "1"

        # Post the form, with some extra headers that are required for proper response
        r = s.post("https://authentication2.caruna.fi/portal" + action, data=svars, headers={
            'Wicket-Ajax': 'true',
            'Wicket-Ajax-BaseURL': 'login',
            'Wicket-FocusedElementId': 'loginWithUserID5',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://authentication2.caruna.fi',
            'Referer': 'https://authentication2.caruna.fi/portal/login'
        })

        # Redirect to the location indicated by the Ajax-Location header
        location = r.headers['Ajax-Location'][1:]
        r = s.get("https://authentication2.caruna.fi/portal" + location)

        # Parse the <meta http-equiv="refresh"> URL and request it (ngPostResponder)
        url = BeautifulSoup(r.content, 'lxml').findAll('meta')[0]['content'][6:]
        r = s.get(url)

        # Parse the form and submit it (would normally be done by JavaScript). Normally it would be enough to have it
        # automatically redirect through all the intermediate URLs, but we need to intercept a particular one in order
        # to grab the Connect2id callback parameters
        soup = BeautifulSoup(r.content, 'lxml')
        action = soup.find('form')['action']
        r = s.post(action, data=utils.get_hidden_form_vars(soup), allow_redirects=False)
        r = s.get(r.headers['Location'], allow_redirects=False)
        openid_login_return_url = r.headers['Location']

        # Extract code, state and session_state
        parsed_url = urlparse(openid_login_return_url)
        parsed_query = parse_qs(parsed_url.query)
        connect2id_params = {
            'code': parsed_query['code'][0],
            'state': parsed_query['state'][0],
            'session_state': parsed_query['session_state'][0],
        }

        # Okay, we now have the Connect2id stuff. Now we can get an OAuth token which is needed for the actual API
        # requests...
        r = s.post(utils.create_caruna_plus_url('/authorization/token'), data=connect2id_params)
        return r.json()
