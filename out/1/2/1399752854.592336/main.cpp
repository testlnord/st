#include <stdio.h>
#include <curl/curl.h>
#include <iostream>
#include <string>
#include <sstream>
#include <utility>
#include <vector>
#include <regex>
#include <thread>

#include <queue>
#include <set>

typedef  std::queue<std::string> QUrl;
typedef  std::set<std::string> SUrl;
SUrl visited_urls;
QUrl urls;
QUrl pages;

size_t write_data(void *buffer, size_t size, size_t nmemb, void *userp)
{
  std::stringstream& stream = *((std::stringstream*)userp);
  char* char_buf = (char*) buffer;

  for (size_t i = 0; i < size * nmemb; ++i)
    stream << char_buf[i]; 

  return size*nmemb;
}



void GetPage(std::string url, QUrl & pages)
{
  CURL *curl;
  CURLcode res;
  std::stringstream stream;

  curl = curl_easy_init();
  if(curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &stream);

    res = curl_easy_perform(curl);
	
    if(res != CURLE_OK)
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
          curl_easy_strerror(res));

    curl_easy_cleanup(curl);
  }
  
  pages.push(stream.str());
}

bool Filter(const std::string& match)
{
  if (match.find('.') != std::string::npos)
    return false;

  if (match.find(':') != std::string::npos)
    return false;

  return true;
}

std::string ToURL(const std::string& match)
{
  return "en.wikipedia.org/wiki/" + match;
}

std::vector<std::string> GetMatches(std::string page)
{
  std::vector<std::string> matches;
  
  const std::string ref = "<a href=\"/wiki/";

  size_t pos = 0;
  while (pos < page.size() && pos != std::string::npos)
  {
    size_t begin = page.find(ref, pos);
    if (begin == std::string::npos)
      break;

    size_t urlStart = begin + ref.size();
    pos = page.find("\"", urlStart);

    auto match = page.substr(urlStart, pos - urlStart);
    matches.push_back(match);
  }

  return matches;
}

void /*std::vector<std::string>*/ GetURLs(std::string page, QUrl& urls, SUrl & visited)
{
   //std::vector<std::string> urls;
  auto matches = GetMatches(page);
  

  for(auto match : matches)
  {
	  if(Filter(match)){
		  if (visited.find(match)== visited.end()){
			  visited.insert(match);
			  urls.push(ToURL(match));
		  }
	  }
      
  }

}


int main(int argc, char** argv)
{
  if (argc < 2)
  {
    std::cout << "no base urls specified" << std::endl;
    return 0;
  }
  urls.push(argv[1]);
  while(visited_urls.size() < 1000){
	  if (pages.empty()){
		  GetPage(urls.back(), pages);		  
		  urls.pop();
	  }
	  GetURLs(pages.back(), urls, visited_urls);
	  pages.pop();
  }
  for(auto url : visited_urls)
    std::cout << url << std::endl;
  
  return 0;
}
