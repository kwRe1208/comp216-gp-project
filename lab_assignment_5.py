"""
COMP216 - Lab Assignment 5

Group: 1
Group Members:
    Handa, Karan
    Ngan, Tsang Kwong
    Patel, Jainam
    Wong, Yu Kwan
    ZHANG, AILIN

Date: February 25, 2021

Description:
This script is used to download images from a list of URLs. It includes
functions to validate the URL, create a filename based on the URL and content
type, write the downloaded content to a file, and clear the download directory.
It also includes a main function that uses these helper functions to download
images both sequentially and concurrently using threading.

"""
import requests
import re
import os
import shutil
import threading
import mimetypes
from time import perf_counter
from urllib.parse import urlparse


def get_single_response(url):
    """
    This function is used to download a single image from a given URL. It validates
    the URL, creates a filename based on the URL and content type, writes the
    downloaded content to a file, and raises an exception if the download fails.
    Parameters:
        url (str): The URL of the image to download.
        Raises:
            ValueError: If the URL is invalid, the file download is incomplete, or
                the file already exists.
            requests.exceptions.RequestException: If the request to the URL fails.
    """
    if not re.match(r'^https?:/{2}\w.+$', url):
        raise ValueError('Invalid URL')

    try:
        with requests.get(url) as response:
            response.raise_for_status()

            # check if file is completely downloaded
            if 'Content-Length' in response.headers:
                if int(response.headers['Content-Length']) != len(response.content):
                    raise ValueError('File download incomplete')

            file_name = create_filename(url, response.headers['Content-Type'])

            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            write_to_file(response, download_dir, file_name)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def create_filename(url, content_type):
    """
    This function is used to create a filename based on the URL and content type.
    Parameters:
        url (str): The URL of the image.
        content_type (str): The content type of the image.
    Returns:
        str: The filename for the image.
    """
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    if '.' not in file_name:
        file_extension = mimetypes.guess_extension(content_type.split(";")[0])
        if file_extension:
            file_name += file_extension
    return file_name


def write_to_file(response, download_dir, file_name):
    """
    This function is used to write the downloaded content to a file.
    Parameters:
        response (requests.Response): The response object from the URL request.
        download_dir (str): The directory to save the downloaded file.
        file_name (str): The name of the file to save the downloaded content.
    Raises:
        ValueError: If the file already exists.
    """
    full_path = os.path.join(download_dir, file_name)
    # check if file exists
    if not os.path.exists(full_path):
        with open(full_path, 'wb') as file:
            file.write(response.content)
            file.close()
    else:
        raise ValueError('File already exists')


def clear_dir(download_dir):
    """
    This function is used to clear the download directory.
    Parameters:
        download_dir (str): The directory to clear.
    """
    if not os.path.exists(download_dir):
        print("Download_dir created successfully")
        return 
    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            raise 'Failed to delete %s. Reason: %s' % (file_path, e)


if __name__ == "__main__":
    """
    This is the main function that uses the helper functions to download images
    both sequentially and concurrently using threading.
    """
    username = os.getlogin()
    download_dir = os.getcwd() + f'/download_dir'
    clear_dir(download_dir)
    img_urls = [
        'https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0', 
        'https://images.unsplash.com/photo-1485833077593-4278bba3f11f', 
        'https://images.unsplash.com/photo-1593179357196-ea11a2e7c119', 
        'https://images.unsplash.com/photo-1526515579900-98518e7862cc', 
        'https://images.unsplash.com/photo-1582376432754-b63cc6a9b8c3', 
        'https://images.unsplash.com/photo-1567608198472-6796ad9466a2', 
        'https://images.unsplash.com/photo-1487213802982-74d73802997c', 
        'https://images.unsplash.com/photo-1552762578-220c07490ea1', 
        'https://images.unsplash.com/photo-1569691105751-88df003de7a4', 
        'https://images.unsplash.com/photo-1590691566903-692bf5ca7493', 
        'https://images.unsplash.com/photo-1497206365907-f5e630693df0', 
        'https://images.unsplash.com/photo-1469765904976-5f3afbf59dfb'
    ]
    
    # Part A - get single url
    get_single_response(img_urls[0])
    
    # Part B
    clear_dir(download_dir)
    timer = perf_counter()
    for url in img_urls:
        get_single_response(url)

    print(f"Time taken to download all images: {perf_counter() - timer} seconds")
    
    # Part C
    clear_dir(download_dir)
    timer = perf_counter()
    threads = []
    for url in img_urls:
        t = threading.Thread(target=get_single_response, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Time taken to download all images using threading: {perf_counter() - timer} seconds")

