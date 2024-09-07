from django.utils import translation


class DefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request already has a language set
        if not request.LANGUAGE_CODE or request.LANGUAGE_CODE == "uz":
            # Default to 'uz' if no other language is set
            user_language = "uz"
        else:
            # Use the language already set
            user_language = request.LANGUAGE_CODE

        response = self.get_response(request)
        translation.deactivate()

        return response
