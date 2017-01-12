# pylint: disable=unused-variable,unused-argument,misplaced-comparison-constant,expression-not-assigned

import os

import pytest
from expecter import expect

from memegen.routes.image import cache

from .conftest import load

TESTS = os.path.dirname(__file__)
ROOT = os.path.dirname(TESTS)
IMAGES = os.path.join(ROOT, 'data', 'images')


def describe_get():

    def describe_visible():

        def with_nominal_text(client):
            path = os.path.join(IMAGES, 'iw', 'hello', 'world' + '.img')
            if os.path.exists(path):
                os.remove(path)

            response = client.get("/iw/hello/world.jpg")

            assert 200 == response.status_code
            assert 'image/jpeg' == response.mimetype
            assert os.path.isfile(path)

        def with_only_1_line(client):
            response = client.get("/iw/hello.jpg")

            assert 200 == response.status_code
            assert 'image/jpeg' == response.mimetype

        @pytest.mark.xfail(os.name == 'nt', reason="Windows has a path limit")
        def with_lots_of_text(client):
            top = "-".join(["hello"] * 20)
            bottom = "-".join(["world"] * 20)
            response = client.get("/iw/" + top + "/" + bottom + ".jpg")

            assert 200 == response.status_code
            assert 'image/jpeg' == response.mimetype

    def describe_hidden():

        def when_jpg(client):
            response = client.get("/_aXcJaGVsbG8vd29ybGQJ.jpg")

            assert 200 == response.status_code
            assert 'image/jpeg' == response.mimetype

    def describe_custom_style():

        def when_provided(client):
            response = client.get("/sad-biden/hello.jpg?alt=scowl")

            assert 200 == response.status_code
            assert 'image/jpeg' == response.mimetype

        def it_redirects_to_lose_alt_when_default_style(client):
            response = client.get("/sad-biden/hello.jpg?alt=default")

            assert 302 == response.status_code
            assert '<a href="/sad-biden/hello.jpg">' in \
                load(response, as_json=False)

        def it_redirects_to_lose_alt_when_unknown_style(client):
            response = client.get("/sad-biden/hello.jpg?alt=__unknown__")

            assert 302 == response.status_code
            assert '<a href="/sad-biden/hello.jpg">' in \
                load(response, as_json=False)

        def it_keeps_alt_after_template_redirect(client):
            response = client.get("/sad-joe/hello.jpg?alt=scowl")

            assert 302 == response.status_code
            assert '<a href="/sad-biden/hello.jpg?alt=scowl">' in \
                load(response, as_json=False)

        def it_keeps_alt_after_text_redirect(client):
            response = client.get("/sad-biden.jpg?alt=scowl")

            assert 302 == response.status_code
            assert '-vote.jpg?alt=scowl">' in \
                load(response, as_json=False)

        def when_url(client):
            url = "http://www.gstatic.com/webp/gallery/1.jpg"
            response = client.get("/sad-biden/hello.jpg?alt=" + url)

            expect(response.status_code) == 200
            expect(response.mimetype) == 'image/jpeg'

        def it_returns_an_error_with_non_image_urls(client):
            url = "http://example.com"
            response = client.get("/sad-biden/hello.jpg?alt=" + url)

            expect(response.status_code) == 415

        def it_handles_png_int32_pixels(client):
            url = "https://raw.githubusercontent.com/jacebrowning/memegen/master/tests/files/201692816359570.jpeg"
            response = client.get("/sad-biden/hello.jpg?alt=" + url)

            expect(response.status_code) == 200
            expect(response.mimetype) == 'image/jpeg'

        def it_handles_jpg_cmyk_pixels(client):
            url = "https://raw.githubusercontent.com/jacebrowning/memegen/master/tests/files/Channel_digital_image_CMYK_color.jpg"
            response = client.get("/sad-biden/hello.jpg?alt=" + url)

            expect(response.status_code) == 200
            expect(response.mimetype) == 'image/jpeg'

        def it_redirects_to_lose_alt_when_unknown_url(client):
            url = "http://example.com/not/a/real/image.jpg"
            response = client.get("/sad-biden/hello.jpg?alt=" + url)

            expect(response.status_code) == 302
            expect(load(response, as_json=False)).contains(
                '<a href="/sad-biden/hello.jpg">')

        def it_redirects_to_lose_alt_when_bad_url(client):
            url = "http:invalid"
            response = client.get("/sad-biden/hello.jpg?alt=" + url)

            expect(response.status_code) == 302
            expect(load(response, as_json=False)).contains(
                '<a href="/sad-biden/hello.jpg">')

    def describe_custom_font():

        def when_provided(client):
            response = client.get("/iw/hello.jpg?font=impact")

            expect(response.status_code) == 200
            expect(response.mimetype) == 'image/jpeg'

        def it_redirects_on_unknown_fonts(client):
            response = client.get("/iw/hello.jpg?font=__unknown__")

            expect(response.status_code) == 302
            expect(load(response, as_json=False)).contains(
                '<a href="/iw/hello.jpg">')

        def it_keeps_font_after_redirect(client):
            response = client.get("/iw/what%3F.jpg?font=impact")

            expect(response.status_code) == 302
            expect(load(response, as_json=False)).contains(
                '<a href="/iw/what~q.jpg?font=impact">')

    def describe_custom_size():

        def it_keeps_size_after_redirect(client):
            response = client.get("/iw/what%3F.jpg?width=67&height=89")

            expect(response.status_code) == 302
            expect(load(response, as_json=False)).contains(
                '<a href="/iw/what~q.jpg?')
            expect(load(response, as_json=False)).contains(
                'width=67')
            expect(load(response, as_json=False)).contains(
                'height=89')

    def describe_preview():

        def it_keeps_flag_after_redirect(client):
            response = client.get("/iw/i am still typi.jpg?preview=true")

            expect(response.status_code) == 302
            expect(load(response, as_json=False)).contains(
                '<a href="/iw/i-am-still-typi.jpg?preview=true">')

    def describe_latest():

        @pytest.fixture()
        def diable_cache():
            cache.disable = True
            cache.items = []

        def when_existing(client, diable_cache):
            cache.disable = False
            client.get("/iw/my-first-meme.jpg")

            response = client.get("/latest.jpg")

            expect(response.status_code) == 302
            expect(load(response, as_json=False)).contains(
                '<a href="http://localhost/iw/my-first-meme.jpg">')

        def when_missing(client, diable_cache):
            response = client.get("/latest.jpg")

            expect(response.status_code) == 302
            expect(load(response, as_json=False)).contains(
                '<a href="http://localhost/custom/your-meme/goes-here.jpg'
                '?alt=https://raw.githubusercontent.com/jacebrowning/memegen/'
                'master/memegen/static/images/missing.png">')

    def describe_redirects():

        def when_missing_dashes(client):
            response = client.get("/iw/HelloThere_World/How-areYOU.jpg")

            assert 302 == response.status_code
            assert '<a href="/iw/hello-there-world/how-are-you.jpg">' in \
                load(response, as_json=False)

        def when_no_text(client):
            response = client.get("/live.jpg")

            assert 302 == response.status_code
            assert '<a href="/live/_/do-it-live!.jpg">' in \
                load(response, as_json=False)

        def when_aliased_template(client):
            response = client.get("/insanity-wolf/hello/world.jpg")

            assert 302 == response.status_code
            assert '<a href="/iw/hello/world.jpg">' in \
                load(response, as_json=False)

        def when_jpeg_extension_without_text(client):
            response = client.get("/iw.jpeg")

            assert 302 == response.status_code
            assert '<a href="/iw.jpg">' in \
                load(response, as_json=False)

        def when_jpeg_extension_with_text(client):
            response = client.get("/iw/hello/world.jpeg")

            assert 302 == response.status_code
            assert '<a href="/iw/hello/world.jpg">' in \
                load(response, as_json=False)

    def describe_errors():

        def when_unknown_template(client):
            response = client.get("/make/sudo/give.me.jpg")

            assert 200 == response.status_code
            assert 'image/jpeg' == response.mimetype
            # unit tests ensure this is a placeholder image

        @pytest.mark.xfail(os.name == 'nt', reason="Windows has a path limit")
        def when_too_much_text_for_a_filename(client):
            top = "hello"
            bottom = "-".join(["world"] * 50)
            response = client.get("/iw/" + top + "/" + bottom + ".jpg")

            assert 414 == response.status_code
            assert {
                'message': "Filename too long."
            } == load(response)
