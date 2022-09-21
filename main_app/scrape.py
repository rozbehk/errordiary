from django.shortcuts import render, redirect
from .models import Challenge
import requests
from bs4 import BeautifulSoup


def scrape(request):
    data = requests.get('https://projecteuler.net/archives;page=10')
    soap = BeautifulSoup(data.content, 'html5lib')
    page_no = soap.find(class_='pagination noprint').find_all('a')[-1].text
    for page in range(1 , int(page_no)+1):
        page =  requests.get(f'https://projecteuler.net/archives;page={page}')
        soap = BeautifulSoup(page.content, 'html5lib')
        last_challenge_no = soap.find_all(class_='id_column')[-1].text
        first_challenge_number = soap.find_all(class_='id_column')[1].text
        for challenge in range(int(first_challenge_number),int(last_challenge_no)+1):
            print(f'page number: {page} challenge number: {challenge}')
            challenge_model = Challenge()
            challenge_data = requests.get(f'https://projecteuler.net/problem={challenge}')
            soap = BeautifulSoup(challenge_data.content, 'html5lib')
            challenge_model.title = soap.find_all('h2')[0].text
            challenge_model.challenge = soap.find_all('h3')[0].text
            challenge_model.description = soap.find_all(class_='challenge_content')[0].text
            challenge_model.save()
        
    return redirect('/')
