from collect import crawler as cr

pagename = "jtbcnews"
from_date = "2018-05-01"
to_date = "2018-05-15"

if __name__ == "__main__" :
    postList = cr.fb_get_post_list(pagename, from_date, to_date)
    print(postList)