from django.shortcuts import render, redirect
from selenium import webdriver
import os
from iotd.models import Item
import re

# Create your views here.

def index(request):
    return render(request, 'index.html')

def detail(request):
    if request.method == "POST":
        userKeyword = request.POST.get('userKeyword')
        userImage = request.FILES.get('userImage')

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 현재 크롬 드라이버
        driver_path = os.path.join(BASE_DIR, 'selenium_drivers', 'chromedriver', 'chromedriver.exe')
        
        driver = webdriver.Chrome(driver_path)
        driver.get('https://www.11st.co.kr')
        driver.find_element_by_name('kwd').send_keys(userKeyword)
        driver.find_element_by_xpath('//button[@id="gnbTxtAd"]').click()

        # 사이트명
        retailer = driver.find_element_by_xpath('//head//meta[@name="description"]').get_attribute('content')

        # 검색결과 있는지 없는지 확인
        try:
            checkNull = driver.find_element_by_xpath('//div[@class="result_null"]')
            checkNull = True
        except:
            checkNull = False

        # 검색 결과가 없을 경우
        if checkNull == True:
            context = {
                'message' : '검색 결과가 없습니다.',
                'userKeyword' : userKeyword,
                'userImage' : userImage
            }
            return render(request, 'detail.html', context)

        # 검색 결과가 있을 경우
        else:
            # 리스트
            lists = driver.find_elements_by_xpath('//div[@id="focusClickPrdArea"]//div[@class="total_listitem"]')
            reslist = []

            # 리스트에서 각 요소 뽑기
            for item in lists:
                # 제품명
                productName = item.find_element_by_class_name('list_info').find_element_by_tag_name('a').text
                # 링크
                link = item.find_element_by_class_name('list_info').find_element_by_tag_name('a').get_attribute('href')
                # 썸네일
                thumbnail_url = item.find_element_by_class_name('photo_wrap').find_element_by_tag_name('img').get_attribute('data-original')
                # 가격
                price = item.find_element_by_class_name('price_detail').text
                # 리뷰 개수
                try:
                    reviewnum = item.find_element_by_class_name('review').text
                except:
                    reviewnum = None
                # 별점
                try:
                    rating = item.find_element_by_class_name('selr_wrap').text
                except:
                    rating = None

                product = Item(
                    productName = productName,
                    retailer = retailer,
                    link = link,
                    thumbnail_url = thumbnail_url,
                    price = price,
                    reviewnum = reviewnum,
                    rating = rating
                )

                product.save()
                reslist.append(product)

            context = {
                'productList' : reslist,
                'retailer' : retailer,
                'userKeyword' : userKeyword,
                'userImage' : userImage
            }

            return render(request, 'detail.html', context)
    else:
        return redirect('iotd:index')

def crawling(request):
    if request.method == "POST":

        modelnum = request.POST.get('modelnum')
        prdlink = request.POST.get('prdlink')

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 현재 크롬 드라이버
        driver_path = os.path.join(BASE_DIR, 'selenium_drivers', 'chromedriver', 'chromedriver.exe')
        
        driver = webdriver.Chrome(driver_path)
        driver.get(prdlink)

        # 사이트명
        retailer = driver.find_element_by_xpath('//head//meta[@name="keywords"]').get_attribute('content')

        # 제품명
        productName = driver.find_element_by_class_name('heading').find_element_by_tag_name('h2').text

        # 링크
        link = prdlink

        # 썸네일
        thumbnail_url = driver.find_element_by_id('thumb').find_element_by_tag_name('img').get_attribute('src')

        # 가격
        price = driver.find_element_by_class_name('sale_price').text + '원'

        # 리뷰 개수
        reviewnum_origin = driver.find_element_by_id('reviewTo').find_element_by_class_name('notice_count').text
        reviewnum = re.sub('[ ,\(\)]', '', reviewnum_origin)

        # 별점
        try:
            rating = driver.find_element_by_id('prdRating').find_element_by_class_name('num').text
        except:
            rating = None

        product = Item(
            modelnum = modelnum,
            productName = productName,
            retailer = retailer,
            link = link,
            thumbnail_url = thumbnail_url,
            price = price,
            reviewnum = reviewnum,
            rating = rating
        )

        product.save()

        return redirect('iotd:index')
    else:
        return render(request, 'crawling.html')