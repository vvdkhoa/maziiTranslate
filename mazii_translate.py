from selenium import webdriver  # https://mylife8.net/install-selenium-and-run-on-windows/
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# https://mylife8.net/install-selenium-and-run-on-windows/
# https://stackoverflow.com/questions/49290704/python-save-html-from-browser
def chrome_scraping(driver, url):
    driver.get(url)
    sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Get ふりがな
    try:
        furigana = soup.select("[class='phonetic-word japanese-char cl-content']")[0].contents[0].strip()
    except:
        furigana = ''

    # Get mean
    try:
        mean = soup.select("[class='mean-fr-word cl-blue']")[0].contents[0]
        mean = mean.replace('◆ ', '')
    except:
        mean = ''

    print("=> Furigana: {}, Mean: {}".format(furigana, mean))
    return {'furigana': furigana, 'mean': mean}


def save_df_to_exel(df, file_name='default_name.xlsx'):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


def main():
    # Open chrome
    driver = webdriver.Chrome()

    # Read word list
    words_list = pd.read_csv("words_list.csv")

    # Create new dataframe
    words_list_out = pd.DataFrame({'Word': pd.Series([], dtype='str'),
                                   'Furigana': pd.Series([], dtype='str'),
                                   'Mean': pd.Series([], dtype='str')})

    for i in range(words_list.shape[0]):
        word = words_list.loc[i][0]
        url = 'https://mazii.net/search?dict=javi&type=w&query=' + word + '&hl=vi-VN'
        scrap = chrome_scraping(driver, url)

        words_list_out.at[i, 'Word'] = word
        words_list_out.at[i, 'Furigana'] = scrap['furigana']
        words_list_out.at[i, 'Mean'] = scrap['mean']

    # Save Excel
    file_name = 'words_list_out_' + datetime.now().strftime("%Y%m%d_%H%M%S.jpg") + '.xlsx'
    save_df_to_exel(words_list_out, file_name)

    # Close chrome
    driver.quit()


if __name__ == '__main__':
    main()
