import feedparser
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz
from ttkbootstrap import Style
import webbrowser

rss_feeds = [
    ('CNBC - Top News', 'https://www.cnbc.com/id/10001147/device/rss/rss.html'),
    ('Benzinga - Analyst Ratings', 'https://www.benzinga.com/analyst-ratings/feed/'),
    ('MarketWatch - Top Stories', 'https://www.marketwatch.com/rss/topstories'),
    ('Bloomberg - Top Financial News', 'https://www.bloomberg.com/feeds/bbiz/sitemap_index.xml'),
    ('Financial Times - Home', 'https://www.ft.com/rss/home'),
    ('Financial Times - International', 'https://www.ft.com/rss/home/international'),
    ('The New York Times - Business', 'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/business/rss.xml'),
    ('MarketBeat - Headlines', 'https://www.marketbeat.com/rss.ashx?type=headlines'),
    ('BabyPips - RSS Feed', 'https://www.babypips.com/feed.rss'),
    ('FXStreet - News', 'https://www.fxstreet.com/rss/news'),
    ('WSJ - Markets', 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml'),
    ('WSJ - World News', 'https://feeds.a.dj.com/rss/RSSWorldNews.xml'),
    ('WSJ - Tech News', 'https://feeds.a.dj.com/rss/RSSWSJD.xml'),
    ('CNBC - Market Insider', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839135'),
    ('CNBC - U.S. Markets', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664'),
    ('CNBC - Market Data', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258'),
    ('CNBC - Investing', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910'),
    ('CNBC - Economy', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19836768'),
    ('CNBC - Real Time', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069'),
    ('CNBC - Top News', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362'),
    ('CNBC - US News', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15837362'),
    ('CNBC - Business', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114')
]

def fetch_news():
    all_news = []
    for feed_name, feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            news_item = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published_parsed,
                'source': feed_name
            }
            all_news.append(news_item)
    return all_news

def update_news():
    news_items = fetch_news()
    news_items.sort(key=lambda x: x['published'], reverse=True)
    utc_zone = pytz.utc
    local_timezone = pytz.timezone('America/Chicago')

    unique_links = set(news_table.item(item)['values'][3] for item in news_table.get_children())
    new_items = []
    for item in news_items:
        if item['link'] not in unique_links:
            unique_links.add(item['link'])
            new_items.append(item)

    for item in reversed(new_items):
        published_time_utc = datetime(*item['published'][:6], tzinfo=utc_zone)  
        published_time_local = published_time_utc.astimezone(local_timezone) 
        published_time_str = published_time_local.strftime('%m-%d %I:%M %p')
        news_table.insert('', 0, values=(item['title'], published_time_str, item['source'], item['link']), tags=('new',))

    root.after(30000, update_news) 

def open_link(event):
    item = news_table.focus()
    if item:
        link = news_table.item(item, 'values')[3]
        webbrowser.open(link)

def on_enter(event):
    news_table.selection_set(news_table.identify_row(event.y))
    news_table.focus(news_table.identify_row(event.y))

def on_leave(event):
    news_table.selection_remove(news_table.focus())

root = tk.Tk()
root.title('Real-time Stock Market News')
style = Style(theme='darkly')
root = style.master

style.configure('Custom.Treeview', rowheight=30) 

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky='nsew')

frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

news_table = ttk.Treeview(frame, columns=('Title', 'Published', 'Source', 'Link'), show='headings', style='Custom.Treeview')
news_table.heading('Title', text='Title')
news_table.heading('Published', text='Published')
news_table.heading('Source', text='Source')
news_table.heading('Link', text='Link')
news_table.column('Title', width=500)
news_table.column('Published', width=100, stretch=False)
news_table.column('Source', width=150, stretch=True)
news_table.column('Link', width=0, stretch=False)
news_table.grid(row=0, column=0, sticky='nsew')

scrollbar = ttk.Scrollbar(frame, orient='vertical', command=news_table.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
news_table.configure(yscrollcommand=scrollbar.set)

news_table.bind('<Double-1>', open_link)
news_table.bind('<Enter>', on_enter)
news_table.bind('<Leave>', on_leave)

update_news()

root.mainloop()
