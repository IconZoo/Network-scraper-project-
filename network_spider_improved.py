# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 20:51:37 2015
Rediscovered 10/03/2017
@author: Mark Kamper Svendsen aka. DJ Awesomepants
"""
from bs4 import BeautifulSoup as bs
import urllib as url
import random as rand
import networkx as nx

class Web_walker():
    def __init__(self, start_url):
        #Saving initial url
        self.start_url  = start_url
        self.start_page = url.request.urlopen(start_url)
        self.start_page = bs(self.start_page, 'html.parser')
        self.page_links = []
        print("[*] The title of the initialization page is: " + self.start_page.title.string + "\n")

#------------------------------------------1------------------------------------------------#        
    #Giving spider the ability to retrieve link
    def links(self):
        self.page_links  = []
        for link in self.start_page.find_all(href = True):
                if 'http' in link.get('href'):
                    self.page_links.append(link.get('href'))                

#------------------------------------------2-------------------------------------------------#
    def crawl(self, steps = 5):
        #Initialization of crawl
        self.links()
        self.pages_on_crawl = ['Page of initialization: ' + self.start_url]
        self.crawl_connections = []
        self.citation_map = {}
        self.citation_map[self.start_url] = {}
        self.citation_map[self.start_url]['Citations'] = []
        for link in self.start_page.find_all(href = True):
                if 'http' in link.get('href'):
                    self.citation_map[self.start_url]['Citations'].append(link.get('href'))
        crawling_links = list(self.page_links)
        for i in range(steps):
            try:
                print('Performing step number: ' + str(i+1))
                if len(crawling_links) == 0:
                    #If spider crawls to a leaf node it will go continue from the start page
                    crawling_links = list(self.links)
                    self.pages_on_crawl.append("Start page: " + self.start_url)
                    print('Hit leaf node - going back to starting page.')
                else:
                    choice = rand.randint(0, len(crawling_links)-1)
                    new_url = crawling_links[choice]
                    #Requesting website content
                    page = url.request.urlopen(new_url)                    
                    websiteHTML = bs(page, 'html.parser')
                    #Reseting and filling crawler links
                    links = []
                    for link in websiteHTML.find_all(href = True):
                        if 'http' in link.get('href'):
                            links.append(link.get('href'))
                    #Adding the visited page to list of visited pages                
                    self.pages_on_crawl.append('Page ' + str(i+1) +": " + new_url)
                    self.citation_map[new_url] = {'Citations':[]}
                    self.citation_map[new_url]['Citations'] = links

            #Introduces additional error - fix this to do something more fair. Maybe random site on crawl? 14/03/2017
            except:
                print('An error was encountered - returning to start page and continuing strawl.')
                crawling_links = list(self.page_links)  
                self.pages_on_crawl.append('Page ' + str(i+1) + ": " + self.start_url)

#-----------------------------------------3--------------------------------------------------#
    #Searching the web close to the page of initialization and saving copy hereof
    def prospect(self):
        self.landscape = nx.Graph()
        if not self.citation_map:
            print("No citation map exist. Execute crawl command first.")
        else:
            #Adding nodes
            for node in self.citation_map:
                self.landscape.add_node(node)
            #Adding edges from lists
            for node in self.landscape.nodes():
                for cite in self.citation_map[node]['Citations']:
                    if cite in self.landscape.nodes():
                        self.landscape.add_edge(node,cite)
        nx.draw(self.landscape)    
        self.pagerank =nx.pagerank(self.landscape)
#------------------------------------------4--------------------------------------------------#
