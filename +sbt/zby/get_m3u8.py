import requests
import json
from pathlib import Path

def get_sbt_m3u8():
    """Fetches the M3U8 link for the SBT live stream from YouTube and saves it to a file."""
    try:
        cookies = {
            'VISITOR_INFO1_LIVE': 'sE6ohXYzpWw',
            'VISITOR_PRIVACY_METADATA': 'CgJVUxIEGgAgJQ%3D%3D',
            'LOGIN_INFO': 'AFmmF2swRgIhAP0XAR0kiByNJ8mNO3_1d4uAP36K-F2EgfkKk6LIAfXoAiEAix_0D-lYR0PBa0UufgwFDytnBjYFNYGXHW5on0iRHZg:QUQ3MjNmekZfTVhYbk9IR2ZueG9sUk95R0JFNndiaWU2YlBsSDBPR1N4NUJ0VjZSTUZGUjM4d1dYRFBQZXZYTzNfaFl5TV9qVld3ZmNkT1JRdU11SmdMOU54QzNaTGp1azg5c1J0QnQ2T19VUXhpVlV6Rld4dzU2YzBEN2hXVzlvaHN6VzdkMnNLRmlURUwyMUtxdWNZSEZ1bmV6ekNfb0ln',
            '__Secure-3PSIDTS': 'sidts-CjIB5H03P_B3jkbwUs4qN8A_H2syLXplEYBwIuB2vfu-1MO3UvghMbyGEmHqkUtgTXd63hAA',
            '__Secure-3PAPISID': 'isFO5K2AVZNBV28n/AB6easbTAR0jTKGOo',
            '__Secure-3PSID': 'g.a000zQgxpS404yF8S67f6MkY7ES3D3VLomstRaNnmo2YJHfuBHxGQ9Zs_pflCIaqrxaoYskU7wACgYKAXUSARYSFQHGX2Miyn4OhQLdzspcCKps20w8TxoVAUF8yKqcz_fMdW_W8VzvySZeJP1D0076',
            'YSC': 'vcWYNhpEcHQ',
            '__Secure-ROLLOUT_TOKEN': 'CPWzidyDidzcRBCXxP3fo_WNAxi8kue-vteOAw%3D%3D',
            '__Secure-3PSIDCC': 'AKEyXzWAV2LLppKwX-iqSVeapo2t8bxBIqBUzpcIkT_HFFDdjogy-d-KdpkkbJxYHq3bZTg78s4',
        }

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
            'authorization': 'SAPISIDHASH 1753428769_be634b9e6033c81a26a24f5fbc992ec2b72f8291_u SAPISID3PHASH 1753428769_be634b9e6033c81a26a24f5fbc992ec2b72f8291_u',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.youtube.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.youtube.com/embed/ABVQXgr2LW4?rel=0&modestbranding=1&enablejsapi=1&showinfo=0&autoplay=0&playsinline=1&widget_referrer=https%3A%2F%2Fwww.sbt.com.br%2F&embed_config=%7B%22autonavRelatedVideos%22%3Afalse%2C%22disableRelatedVideos%22%3Atrue%2C%22relatedChannels%22%3A%5B%5D%2C%22relatedVideos%22%3A%5B%5D%2C%22adsConfig%22%3A%7B%22disableAds%22%3Atrue%7D%2C%22enableIma%22%3Atrue%7D&origin=https%3A%2F%2Fyoutube-player.sbt.com.br&widgetid=1&forigin=https%3A%2F%2Fyoutube-player.sbt.com.br%2F%3FvideoID%3DABVQXgr2LW4%26t%3D0%26adunit%3D%2F1011235%2FSBT_Videos%2FEspeciais%2FSBT_Live%2Fvideo&aoriginsup=1&aorigins=https%3A%2F%2Fwww.sbt.com.br&gporigin=https%3A%2F%2Fwww.sbt.com.br%2F&vf=6',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'active',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-browser-channel': 'stable',
            'x-browser-copyright': 'Copyright 2025 Google LLC. All rights reserved.',
            'x-browser-validation': '6h3XF8YcD8syi2FF2BbuE2KllQo=',
            'x-browser-year': '2025',
            'x-client-data': 'CIS2yQEIo7bJAQipncoBCKmVywEIlqHLAQiko8sBCIWgzQEIiv3OARjh4s4B',
            'x-goog-authuser': '0',
            'x-goog-visitor-id': 'CgtzRTZvaFhZenBXdyiZ5ozEBjIKCgJVUxIEGgAgJQ%3D%3D',
            'x-origin': 'https://www.youtube.com',
            'x-youtube-bootstrap-logged-in': 'true',
            'x-youtube-client-name': '56',
            'x-youtube-client-version': '1.20250722.00.00',
        }

        params = {
            'prettyPrint': 'false',
        }

        json_data = {
            'videoId': 'ABVQXgr2LW4',
            'context': {
                'client': {
                    'hl': 'en',
                    'gl': 'BR',
                    'remoteHost': '154.205.156.51',
                    'deviceMake': '',
                    'deviceModel': '',
                    'visitorData': 'CgtzRTZvaFhZenBXdyiZ5ozEBjIKCgJVUxIEGgAgJQ%3D%3D',
                    'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36,gzip(gfe)',
                    'clientName': 'WEB_EMBEDDED_PLAYER',
                    'clientVersion': '1.20250722.00.00',
                    'osName': 'Windows',
                    'osVersion': '10.0',
                    'originalUrl': 'https://www.youtube.com/embed/ABVQXgr2LW4?rel=0&modestbranding=1&enablejsapi=1&showinfo=0&autoplay=0&playsinline=1&widget_referrer=https%3A%2F%2Fwww.sbt.com.br%2F&embed_config=%7B%22autonavRelatedVideos%22%3Afalse%2C%22disableRelatedVideos%22%3Atrue%2C%22relatedChannels%22%3A%5B%5D%2C%22relatedVideos%22%3A%5B%5D%2C%22adsConfig%22%3A%7B%22disableAds%22%3Atrue%7D%2C%22enableIma%22%3Atrue%7D&origin=https%3A%2F%2Fyoutube-player.sbt.com.br&widgetid=1&forigin=https%3A%2F%2Fyoutube-player.sbt.com.br%2F%3FvideoID%3DABVQXgr2LW4%26t%3D0%26adunit%3D%2F1011235%2FSBT_Videos%2FEspeciais%2FSBT_Live%2Fvideo&aoriginsup=1&aorigins=https%3A%2F%2Fwww.sbt.com.br&gporigin=https%3A%2F%2Fwww.sbt.com.br%2F&vf=6',
                    'platform': 'DESKTOP',
                    'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
                    'configInfo': {
                        'appInstallData': 'CJnmjMQGEPyyzhwQipeAExC72c4cEKmZgBMQlP6wBRC9tq4FELjkzhwQibDOHBDds88cEMXLzxwQ6rvPHBCHrM4cEMzAzxwQn6HPHBCly88cEL2ZsAUQzqzPHBCZjbEFEMn3rwUQiIewBRDyxM8cEPDizhwQt-r-EhCvj_8SEPzOzxwQ0-GvBRCI468FEJmYsQUQ8JywBRD2us8cEOO-zxwQxcPPHBDHyM8cEJOGzxwQ9quwBRDevM4cEOHKzxwQktHPHBC52c4cEIHNzhwQ2vfOHBD2y88cEMrKzxwQsIbPHBCYuc8cEJ7QsAUQzN-uBRC9irAFEOHLzxwQioKAExCBs84cEO_EzxwQABDmxc8cEKTPzxwqHENBTVNEeFVNLVpxLURPSGRoUXJMM0E0ZEJ3PT0%3D',
                    },
                    'browserName': 'Chrome',
                    'browserVersion': '138.0.0.0',
                    'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'deviceExperimentId': 'ChxOelV6TURreE9URTRORGsyTWpNME9Ea3lPQT09EJnmjMQGGJnmjMQG',
                    'rolloutToken': 'CPWzidyDidzcRBCXxP3fo_WNAxi8kue-vteOAw%3D%3D',
                    'screenWidthPoints': 968,
                    'screenHeightPoints': 545,
                    'screenPixelDensity': 2,
                    'screenDensityFloat': 1.5,
                    'utcOffsetMinutes': 480,
                    'userInterfaceTheme': 'USER_INTERFACE_THEME_LIGHT',
                    'connectionType': 'CONN_CELLULAR_3G',
                    'timeZone': 'Asia/Shanghai',
                    'playerType': 'UNIPLAYER',
                    'tvAppInfo': {
                        'livingRoomAppMode': 'LIVING_ROOM_APP_MODE_UNSPECIFIED',
                    },
                    'clientScreen': 'EMBED',
                },
                'user': {
                    'lockedSafetyMode': False,
                },
                'request': {
                    'useSsl': True,
                    'internalExperimentFlags': [],
                    'consistencyTokenJars': [],
                },
                'thirdParty': {
                    'embeddedPlayerContext': {
                        'ancestorOrigins': [
                            'https://youtube-player.sbt.com.br',
                            'https://www.sbt.com.br',
                        ],
                        'embeddedPlayerEncryptedContext': 'AD5ZzFR9is8ZoUh-ly5sGZSuOrQmKSIp7h_8WZSTDRYJ_2kq3CwvxTS6bhs7qztxmSeBEFNuDeUpdXivmJGcIhuiV6ZL61WNBlbh1K752_M3deI9F7JA8_M_WCsVhRx5vCI_VcwhR-yQJqNe9qbhB8KDANOcxbbff1oDLrMMGdS1KJqiD6OgaZQwIboNGxM1yjHaHWVLmwTbeUFncn6OfWjjhrzal-rh4zIiLbie-mDfbgCcu_XgH0wYwgJlJ1CFWbaCc2oS2u9jhBPlmn1EPUIKFoGpx8PSbVQ',
                        'ancestorOriginsSupported': True,
                        'visibilityFraction': 0,
                        'visibilityFractionSource': 'EMBEDDED_PLAYER_VISIBILITY_FRACTION_SOURCE_INTERSECTION_OBSERVER',
                        'autoplayBrowserPolicy': 'AUTOPLAY_BROWSER_POLICY_UNSPECIFIED',
                        'autoplayIntended': False,
                        'autoplayStatus': 'AUTOPLAY_STATUS_NOT_ATTEMPTED',
                    },
                    'embedUrl': 'https://youtube-player.sbt.com.br/',
                },
                'clientScreenNonce': 'Q6yXljb4rji2npE3',
                'adSignalsInfo': {
                    'params': [
                        {
                            'key': 'dt',
                            'value': '1753428764518',
                        },
                        {
                            'key': 'flash',
                            'value': '0',
                        },
                        {
                            'key': 'frm',
                            'value': '2',
                        },
                        {
                            'key': 'u_tz',
                            'value': '480',
                        },
                        {
                            'key': 'u_his',
                            'value': '1',
                        },
                        {
                            'key': 'u_h',
                            'value': '960',
                        },
                        {
                            'key': 'u_w',
                            'value': '1707',
                        },
                        {
                            'key': 'u_ah',
                            'value': '960',
                        },
                        {
                            'key': 'u_aw',
                            'value': '1707',
                        },
                        {
                            'key': 'u_cd',
                            'value': '24',
                        },
                        {
                            'key': 'bc',
                            'value': '31',
                        },
                        {
                            'key': 'bih',
                            'value': '-12245933',
                        },
                        {
                            'key': 'biw',
                            'value': '-12245933',
                        },
                        {
                            'key': 'brdim',
                            'value': '0,0,0,0,1707,0,1707,960,1707,821,1.125,1.125',
                        },
                        {
                            'key': 'vis',
                            'value': 'prerender',
                        },
                        {
                            'key': 'wgl',
                            'value': 'true',
                        },
                        {
                            'key': 'ca_type',
                            'value': 'image',
                        },
                    ],
                },
            },
            'playbackContext': {
                'contentPlaybackContext': {
                    'currentUrl': '/embed/ABVQXgr2LW4?rel=0&modestbranding=1&enablejsapi=1&showinfo=0&autoplay=0&playsinline=1&widget_referrer=https%3A%2F%2Fwww.sbt.com.br%2F&embed_config=%7B%22autonavRelatedVideos%22%3Afalse%2C%22disableRelatedVideos%22%3Atrue%2C%22relatedChannels%22%3A%5B%5D%2C%22relatedVideos%22%3A%5B%5D%2C%22adsConfig%22%3A%7B%22disableAds%22%3Atrue%7D%2C%22enableIma%22%3Atrue%7D&origin=https%3A%2F%2Fyoutube-player.sbt.com.br&widgetid=1&forigin=https%3A%2F%2Fyoutube-player.sbt.com.br%2F%3FvideoID%3DABVQXgr2LW4%26t%3D0%26adunit%3D%2F1011235%2FSBT_Videos%2FEspeciais%2FSBT_Live%2Fvideo&aoriginsup=1&aorigins=https%3A%2F%2Fwww.sbt.com.br&gporigin=https%3A%2F%2Fwww.sbt.com.br%2F&vf=6',
                    'vis': '0',
                    'splay': False,
                    'autoCaptionsDefaultOn': False,
                    'autonavState': 'AUTONAV_STATE_DISABLED',
                    'html5Preference': 'HTML5_PREF_SECURE_VIDEO_REQUIRED',
                    'lactMilliseconds': '20332',
                    'playerWidthPixels': 853,
                    'playerHeightPixels': 480,
                },
            },
            'racyCheckOk': True,
            'contentCheckOk': True,
        }

        response = requests.post(
            'https://www.youtube.com/youtubei/v1/player',
            params=params,
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        m3u8_url = data['streamingData']['hlsManifestUrl']

        output_data = {
            "channel": "SBT",
            "m3u8_url": m3u8_url
        }
        path = Path(__file__).parent
        with open(path / 'sbt.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)

        print(f"Successfully fetched M3U8 link and saved to sbt.json")
        print(json.dumps(output_data, indent=4, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except (KeyError, IndexError) as e:
        print(f"Could not find the M3U8 link in the response. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':

    get_sbt_m3u8()