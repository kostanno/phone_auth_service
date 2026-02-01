from rest_framework.throttling import SimpleRateThrottle


class RequestCodeThrottle(SimpleRateThrottle):
    scope = 'request_code'

    def get_cache_key(self, request, view):
        phone = request.data.get('phone_number')
        if phone:
            return self.cache_format % {
                'scope': self.scope,
                'ident': phone
            }
        return None


class VerifyCodeThrottle(SimpleRateThrottle):
    scope = 'verify_code'

    def get_cache_key(self, request, view):
        phone = request.data.get('phone_number')
        if phone:
            return self.cache_format % {
                'scope': self.scope,
                'ident': phone
            }
        return None