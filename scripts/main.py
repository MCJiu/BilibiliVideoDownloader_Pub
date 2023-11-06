import download_video
import download_bangumi
from menu import main_menu
from merge import mergeVA
# --main--
cookie = {}

print("\033[36m" +
      "Welcome to use Bilibili video downloader developed by MCJiu!" +
      "\033[0m")
print("\033[36m" + "Have fun!" + "\033[0m")
print("")

while True:

    main_menu()
    print("")
    inputChoice = input("\033[36m" + "Your choice: " + "\033[0m")
    choice = inputChoice[0].lower()  #choice只能是小写
    if choice == "a":
        str_SESSDATA = input("\033[36m" +
                             "Please input your Bilibili SESSDATA: " +
                             "\033[0m")
        cookie = {"SESSDATA": str_SESSDATA}
    elif choice == "b":
        bvid = input("\033[36m" + "Please input BVID: " + "\033[0m")
        bvid = bvid[:12]
        cid = download_video.get_cid_list(bvid, cookie=cookie)
        if cid != 0:
            urls = download_video.get_streamURL(bvid, cid, cookie)
            if urls != 0:
                if download_video.downloader(urls):
                    print("\033[32;1m" + "Download successfully!" + "\033[0m")
                    print("\033[32;1m" + "Merging!" + "\033[0m")
                    mergeVA("video.mp4", "audio.wav")
                    print("\033[32;1m" + "Merged!" + "\033[0m")
                else:
                    print("\033[31;1m" + "Download faild!" + "\033[0m")
    elif choice == "c":
        while True:
            try:
                ep_id = int(
                    input("\033[36m" + "Please input ep_id: " + "\033[0m"))
                break
            except ValueError:
                print("\033[31;1m" +
                      "ep_id must be an integer! Please try again" + "\033[0m")
        urls = download_bangumi.get_streamURL(ep_id, cookie=cookie)
        if urls != 0:
            if download_bangumi.downloader(urls):
                print("\033[32;1m" + "Download successfully!" + "\033[0m")
                print("\033[32;1m" + "Merging!" + "\033[0m")
                mergeVA("video.mp4", "audio.wav")
                print("\033[32;1m" + "Merged!" + "\033[0m")
            else:
                print("\033[31;1m" + "Download faild!" + "\033[0m")
    elif choice == "d":
        exit()
    else:
        print("\033[1;31m" + "Invalid input!" + "\033[0m")
