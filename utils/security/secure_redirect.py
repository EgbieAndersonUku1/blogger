from flask import request, url_for, redirect
from urllib.parse import urlparse, urljoin


def is_safe_url(target):

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def url_secure_redirect(url_to_redirect_to, go_to_referred_url=False):

    if is_safe_url(url_to_redirect_to):
        if not go_to_referred_url:
            return redirect(url_for(url_to_redirect_to))
        return redirect(url_for(url_to_redirect_to, next=request.url))
    return redirect(url_for(request.url))