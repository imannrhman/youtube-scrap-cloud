import fuckit
import time
from selenium.webdriver.common.by import By


def get_video_result(driver, query):
    youtube_data = []

    driver.get('https://www.youtube.com/results?search_query={}'.format(query))
    time.sleep(1)

    prev_size = 0
    size_rendered_video = 1
    y = 500
    while prev_size != size_rendered_video:
        prev_size = size_rendered_video
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 500
        time.sleep(1)
        size_rendered_video = len(driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer"))

    videos = driver.find_elements(By.CSS_SELECTOR, "#contents > ytd-video-renderer")

    for video in videos:
        text = video.find_element(By.CSS_SELECTOR, ".text-wrapper.style-scope.ytd-video-renderer")
        title = text.find_element(By.CSS_SELECTOR, ".title-and-badge.style-scope.ytd-video-renderer").text
        link = text.find_element(By.CSS_SELECTOR, '.title-and-badge.style-scope.ytd-video-renderer a') \
            .get_attribute('href')

        channel_name = text.find_element(By.CSS_SELECTOR, '.long-byline').text
        channel_link = text.find_element(By.CSS_SELECTOR, '#text > a').get_attribute('href')

        # Data can be null
        time_video = None
        thumbnail = None
        channel_image = None
        time_published = None
        snippet = None

        views = None
        verified_badge = False
        extensions = None
        with fuckit:
            views = video.find_element(By.CSS_SELECTOR, '.style-scope ytd-video-meta-block').text.split('\n')[0]

        with fuckit:
            time_published = video.find_element(By.CSS_SELECTOR, '.style-scope ytd-video-meta-block') \
                .text.split('\n')[1]

        with fuckit:
            thumbnail = video.find_element(By.CSS_SELECTOR, '#thumbnail > yt-image > img') \
                .get_attribute('src')

        with fuckit:
            channel_image = text.find_element(By.CSS_SELECTOR, "#img") \
                .get_attribute('src')

        with fuckit:
            snippet = video.find_element(By.CSS_SELECTOR, '.metadata-snippet-container.ytd-video-renderer').text

        with fuckit:
            time_video = video.find_element(By.CSS_SELECTOR, '#text').text

        with fuckit:
            extensions = video.find_element(By.CSS_SELECTOR,
                                            '.badge-style-type-simple.ytd-badge-supported-renderer').text

        with fuckit:
            if video.find_element(By.CSS_SELECTOR,
                                  '.badge-style-type-verified.ytd-badge-supported-renderer') is not None:
                verified_badge = True
            else:
                verified_badge = False

        if thumbnail != None:
            youtube_data.append({
                'title': title,
                'link': link,
                'thumbnail': thumbnail,
                'time_video': time_video,
                'channel': {'channel_name': channel_name, 'channel_link': channel_link, 'channel_image': channel_image},
                'views': views,
                'time_published': time_published,
                'snippet': snippet,
                'verified_badge': verified_badge,
                'extensions': extensions,
            })

    driver.close()
    return youtube_data


def get_comment_video(driver, link):
    driver.get(link)
    time.sleep(2)

    prev_size = 0
    size_rendered_comment = 1
    elem_scroll = driver.find_element(By.XPATH, "/html/body/ytd-app/ytd-third-party-manager")
    while prev_size != size_rendered_comment:
        prev_size = size_rendered_comment
        elem_scroll.location_once_scrolled_into_view
        time.sleep(2)
        size_rendered_comment = len(driver.find_elements(By.XPATH,
                                                         "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer"))

    comments = driver.find_elements(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div["
                                              "1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div["
                                              "3]/ytd-comment-thread-renderer")

    comments = []
    replies = []
    for comment in comments:

        with fuckit:
            reply_elem = comment.find_element(By.XPATH,
                                              "div/ytd-comment-replies-renderer/div[1]/div[1]/div["
                                              "1]/ytd-button-renderer")
            reply_elem.click()
            time.sleep(2)
        replies_elem = driver.find_elements(By.XPATH,
                                            "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div["
                                            "1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div["
                                            "3]/ytd-comment-thread-renderer/div/ytd-comment-replies-renderer/div[1]/div["
                                            "2]/div[1]/ytd-comment-renderer/div[3]/div[2]/div["
                                            "2]/ytd-expander/div/yt-formatted-string")
        for reply_elem in replies_elem:
            replies.append(reply_elem.text)

        comment_text = comment.find_element(By.XPATH,
                                            "ytd-comment-renderer/div[3]/div[2]/div["
                                            "2]/ytd-expander/div/yt-formatted-string").text
        comments.append({
            "comment": comment_text,
            "reply": replies
        })
    driver.close()
    return comments
