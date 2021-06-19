import scrapy
from scrapy.http import HtmlResponse
from instaparser.spiders.some_funcs import read_password
import re
from urllib.parse import urlencode
import json
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstaparserruSpider(scrapy.Spider):
    name = 'instaparserru'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login = 'ol.zy'
    insta_pass = read_password('file.txt')
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    parsed_user = 'ir0nhulk'
    posts_hash = '7ea6ae3cf6fb05e73fcbe1732b1d2a42'
    post_hash = '971f52b26328008c768b7d8e4ac9ce3c'

    #   user_hash = 'd4d88dc1500312af6f937f7b804c68c3'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link, method='POST', callback=self.user_parse_after_login,
                                 formdata={'username': self.insta_login, 'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf_token})

    def user_parse_after_login(self, response: HtmlResponse):
        j_body = response.json()
        print()
        if j_body.get('authenticated'):
            yield response.follow(f'/{self.parsed_user}', callback=self.user_data_parse,
                                  cb_kwargs={'username': self.parsed_user})

    def user_data_parse(self, response: HtmlResponse,
                        username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,  # Формируем словарь для передачи даных в запрос
                     'first': 12}
        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)})
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        print()
        for post in posts:
            post_shortcode = post['node']['shortcode']
            # variables = {'shortcode': post_shortcode, "child_comment_count": 3, "fetch_comment_count": 40,
            #              'parent_comments_count': 24, 'has_threaded_comments': 'true'}
            variables = f'{{"shortcode":"{post_shortcode}","child_comment_count":3,"fetch_comment_count":40,' \
                        '"parent_comment_count":24,"has_threaded_comments":true}'
            url_post = f'{self.graphql_url}query_hash={self.post_hash}&variables={variables}'
            print()
            yield response.follow(url_post, callback=self.post_parse, cb_kwargs={'parsed_user': user_id})

    # идем в пост, выбираем из него комменты и проходимся по ним
    # сначала я сделала реализацию с заходом к каждому пользователю (использовала query_hash для пользователя, но потом поняла, что по
    # получаемой ссылке нет информации, которую нельзя получить из комментария! поэтому информацию о пользователе стала брать сразу из комментария
    def post_parse(self, response: HtmlResponse, parsed_user):
        j_data = response.json()
        comments = j_data.get('data').get('shortcode_media').get('edge_media_to_parent_comment').get('edges')
        user_number = 0
        if comments:
            for comment in comments:
                if user_number <= min(len(comments), 20):
                    user_number += 1
                    user_id = comment.get('node').get('owner').get('id')
                    # поля с таким именем не нашла нигде, поэтому беру username
                    # был еще вариант брать имя-фамилию со страницы пользователя по xpath, но я решила так не делать
                    fullname = comment.get('node').get('owner').get('username')
                    user_photo_link = comment.get('node').get('owner').get('profile_pic_url')
                    user_link = f"{self.start_urls[0]}{fullname}/"
                    item = InstaparserItem(user_photo_link=user_photo_link, user_link=user_link, user_id=user_id,
                                           fullname=fullname, parsed_user=parsed_user)
                    yield item
                else:
                    break

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
