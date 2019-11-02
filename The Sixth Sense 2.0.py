#from RtpPacket import RtpPacket
from tkinter import *
import tkinter.messagebox
import socket
import re
import cv2
import rtsp
import time
from _thread import *
from PIL import ImageTk, Image


class temp:
    truck = 0
    server_ports = [0, 0]
    session_name = ''
    session_timeout = ''
    rtp1_info = []
    rtp2_info = []


IP = "192.168.100.1"  # IP address of your cam
PORT = 554
ADR = "rtsp://192.168.100.1"  # username, passwd, etc.
USER_AGENT = "LibVLC/3.0.0-git (LIVE555 Streaming Media v2016.11.28)"
TIME_OUT = 3
CLIENT_RTSP_PORT = 50006
CLIENT_RTP_PORT = 57412
CLIENT_RTCP_PORT = 57413
# port = 16 bit

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.settimeout(TIME_OUT)

rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rtsp_socket.settimeout(TIME_OUT)

rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rtp_socket.settimeout(TIME_OUT)

rtcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rtcp_socket.settimeout(TIME_OUT)

####->Root

#root =  tkinter.Toplevel()
root = tkinter.Tk()

root.title("The Sixth Sense ")
root.geometry("500x500+600+100")

####Root<-


####->main

#selectedpicture = ImageTk.PhotoImage(file="Logo.jpg")
path = r"C:\Users\Guy Laniado\PycharmProjects\The Sixth Sense\venv\Logo.jpg"
selectedpicture = ImageTk.PhotoImage(Image.open(path))

main = tkinter.Canvas(root, width=500, height=500, bg='BLACK')
main.grid(row=0)

main.create_image(250, 0, anchor=N, image=selectedpicture)


####->main


####->status bar

status_bar = Label(root, text="Wating", bd=1, relief=SUNKEN, anchor=W, bg='BLACK', fg='WHITE')
status_bar.grid(row=0, sticky=S)


# status_bar.pack(side = BOTTOM,fill = X)


####status bar<-

def create_8888_socket():
    status_bar['text'] = "Try to connect"
    root.update_idletasks()

    try:

        tcp_socket.connect((IP, 8888))


    except Exception as e:
        print (e)
        status_bar['text'] = str(e)
        root.update_idletasks()

    else:
        status_bar['text'] = "Connected"
        root.update_idletasks()
        text = "434d445f415247414e414c5953455f676574497257696474683a"
        tcp_socket.send(text.encode())
        start_new_thread(tcp_socket_recv, ())


def tcp_socket_recv():
    while True:

        try:
            recst = tcp_socket.recv(20480)
            if recst:
                print("##############TCP_socket:")
                recst = recst.decode("ISO-8859-1")
                recst_str = str(recst)
                print(recst)

        except Exception as e:
            print (e)


        else:
            print("again")


def create_socket():
    status_bar['text'] = "Try to connect"
    root.update_idletasks()
    # rtsp_socket.bind(("0.0.0.0", CLIENT_RTSP_PORT))

    try:

        rtsp_socket.connect((IP, PORT))
    #    except rtsp_socket.timeout:

    #    except rtsp_socket.error as socketerror:

    except Exception as e:
        print (e)
        status_bar['text'] = str(e)
        root.update_idletasks()

    else:
        status_bar['text'] = "Connected"
        root.update_idletasks()
    # addr, port = s.getsockname()


def send_options():
    print ("*** SENDING OPTIONS ***")
    status_bar['text'] = "SENDING->OPTIONS"
    root.update_idletasks()
    cseq = 2
    opt = "OPTIONS {}:{}/stream0 RTSP/1.0\r\nCSeq: {}\r\nUser-Agent: {}\r\n\r\n".format(ADR, PORT, cseq, USER_AGENT)

    try:
        rtsp_socket.send(opt.encode())
    except Exception as e:
        print (e)
        status_bar['text'] = str(e)
        root.update_idletasks()

    else:

        recst = rtsp_socket.recv(4096)
        recst = recst.decode("utf-8")
        status_bar['text'] = recst
        root.update_idletasks()


def send_describe():
    print ("*** SENDING DESCRIBE ***")
    status_bar['text'] = "SENDING->DESCRIBE"
    root.update_idletasks()
    cseq = 3
    dest = "DESCRIBE {}:{}/stream0 RTSP/1.0\r\nCSeq: {}\r\nUser-Agent: {}\r\nAccept: application/sdp\r\n\r\n".format(
        ADR, PORT, cseq, USER_AGENT)

    try:
        rtsp_socket.send(dest.encode())
    except Exception as e:
        print (e)
        status_bar['text'] = str(e)
        root.update_idletasks()

    else:

        recst = rtsp_socket.recv(4096)
        recst = recst.decode("utf-8")
        status_bar['text'] = recst
        root.update_idletasks()

        temp.truck = re.search('a=control:track(.+?)\r\n', recst).group(1)


def send_setup():
    print ("*** SENDING SETUP ***")
    status_bar['text'] = "SENDING->SETUP"
    root.update_idletasks()
    cseq = 1
    setup = "SETUP {}/stream0/track{} RTSP/1.0\r\nCSeq: {}\r\nUser-Agent: {}\r\nTransport: RTP/AVP;unicast;client_port={}-{}\r\n\r\n".format(
        ADR, temp.truck, cseq, USER_AGENT, CLIENT_RTP_PORT, CLIENT_RTCP_PORT)

    try:
        rtsp_socket.send(setup.encode())
    except Exception as e:
        print (e)
        status_bar['text'] = str(e)
        root.update_idletasks()

    else:

        recst = rtsp_socket.recv(4096)
        recst = recst.decode("utf-8")
        recst_str = str(recst)

        ###------------>Look for " server_port= "
        server_ports = re.search('server_port=(.+?)\r\n', recst_str).group(1)
        server_ports_list = server_ports.split('-')
        temp.server_ports[0] = server_ports_list[0]
        temp.server_ports[1] = server_ports_list[1]
        ###Look for " server_port= "  <--------------------

        ###------------>Look for  " Session: "
        session = re.search('Session: (.+?)\r\n', recst_str).group(1)
        session_list = session.split(';')
        temp.session_name = session_list[0]

        timeout = session_list[1].split('=')
        temp.session_timeout = timeout[1]

        ###Look for " Session: "  <-----------------------

        status_bar['text'] = recst
        root.update_idletasks()


def send_play():
    print ("*** SENDING PLAY ***")
    status_bar['text'] = "SENDING->PLAY"
    root.update_idletasks()
    cseq = 1
    setup = "PLAY {}/stream0 RTSP/1.0\r\nCSeq: {}\r\nUser-Agent: {}\r\nSession: {}\r\nRange: npt=0.000-\r\n\r\n".format(
        ADR, cseq, USER_AGENT, temp.session_name)

    try:
        rtsp_socket.send(setup.encode())
    except Exception as e:
        print (e)
        status_bar['text'] = str(e)
        root.update_idletasks()

    else:

        recst = rtsp_socket.recv(4096)

        recst_str = str(recst)

        ###------------>Look for " RTP-Info: "
        try:
            print(recst_str)
            rtp_info = re.search('RTP-Info: (.+?)\r\n', recst_str).group(1)
        except Exception as e:
            print (e)
        else:
            rtp_info_list = rtp_info.split(',')

            temp.rtp1_info = rtp_info_list[0].split(';')
            temp.rtp2_info = rtp_info_list[1].split(';')
            status_bar['text'] = recst
            root.update_idletasks()


def send_teardown():
    print ("*** SENDING TEARDOWN ***")
    status_bar['text'] = "SENDING->TEARDOWN"
    root.update_idletasks()
    cseq = 1
    setup = "TEARDOWN {}/stream0 RTSP/1.0\r\nCSeq: {}\r\nUser-Agent: {}\r\nSession: {}\r\n\r\n".format(ADR, cseq,
                                                                                                       USER_AGENT,
                                                                                                       temp.session_name)

    try:
        rtsp_socket.send(setup.encode())
    except Exception as e:
        print (e)
        status_bar['text'] = str(e)
        root.update_idletasks()

    else:

        recst = rtsp_socket.recv(4096)
        recst = recst.decode("utf-8")
        recst_str = str(recst)
        status_bar['text'] = recst
        root.update_idletasks()

    # N - RTP


# N+1 - RTCP

def create_socket_udp():
    status_bar['text'] = "Try to connect"
    root.update_idletasks()

    try:
        massage = "cefaedfe"
        rtp_socket.bind(("0.0.0.0", CLIENT_RTP_PORT))
        rtcp_socket.bind(("0.0.0.0", CLIENT_RTCP_PORT))
        rtp_socket.sendto(bytes(massage, "utf-8"), (IP, int(temp.server_ports[0])))
        rtcp_socket.sendto(bytes(massage, "utf-8"), (IP, int(temp.server_ports[1])))
        rtp_socket.connect((IP, int(temp.server_ports[0])))
        rtcp_socket.connect((IP, int(temp.server_ports[1])))

    except Exception as e:
        print (e)
        status_bar['text'] = str(e)
        root.update_idletasks()

    else:
        start_new_thread(rtp_socket_recv, ())
        start_new_thread(rtcp_socket_recv, ())
        status_bar['text'] = "Connected"
        root.update_idletasks()


def rtp_socket_recv():
    while True:

        try:
            recst = rtp_socket.recv(20480)
            if recst:
                print("##############rtp_socket:")
                # recst = recst.decode("utf-8")
                # recst_str = str(recst)
                # print(recst+"ss")
                rtpPacket = RtpPacket()

                rtpPacket.decode(recst)

                currFrameNbr = rtpPacket.seqNum()

                print ("Current Seq Num: " + str(currFrameNbr))

        except Exception as e:
            print ("no rtp_socket")


        else:
            print("again")


def rtcp_socket_recv():
    while True:

        try:
            recst = rtcp_socket.recv(20480)
            if recst:
                print("#############rtcp_socket:")
                # recst = recst.decode("utf-8")
                # recst_str = str(recst)
                # print(recst+"ss")
                rtpPacket = RtpPacket()

                rtpPacket.decode(recst)

                version = rtpPacket.version()

                print ("Current version: " + str(version))

                currFrameNbr = rtpPacket.seqNum()

                print ("Current Seq Num: " + str(currFrameNbr))

                timestamp = rtpPacket.timestamp()

                print ("Current timestamp Num: " + str(timestamp))

        except Exception as e:
            print ("no rtcp_socket")

        else:
            print("again")



def server_information():
    message = "IP=" + str(IP) + "    ;PORT=" + str(PORT) + "    ;ADR=" + str(ADR) + "    ;TIME_OUT=" + str(TIME_OUT)
    tkinter.messagebox.showinfo("Server Information", message)


############ submenu1################

def preview():
    cap = cv2.VideoCapture('Tv sapir.mp4')

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")
    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Preview', gray)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


def stream():
    adress = temp.rtp1_info[0].split('=')
    print(adress[1])
    adress = temp.rtp2_info[0].split('=')
    print(adress[1])


############main###############


menu = Menu(root)
root.config(menu=menu)
submenu0 = Menu(menu)
menu.add_cascade(label="Connection", menu=submenu0)
submenu0.add_command(label="Create 8888 Socket", command=create_8888_socket)
submenu0.add_command(label="Create Socket", command=create_socket)
submenu0.add_command(label="Send->OPTIONS", command=send_options)

submenu0.add_command(label="Send->DESCRIBE", command=send_describe)

submenu0.add_command(label="Send->SETUP", command=send_setup)
submenu0.add_command(label="Send->PLAY", command=send_play)
submenu0.add_command(label="Send->TEARDOWN", command=send_teardown)

submenu0.add_separator()
submenu0.add_command(label="Create_socket_udp", command=create_socket_udp)

submenu0.add_separator()
submenu0.add_command(label="Server Information", command=server_information)

####### ------->submenu1
submenu1 = Menu(menu)

menu.add_cascade(label="Display", menu=submenu1)
submenu1.add_command(label="Preview", command=preview)
submenu1.add_command(label="Stream", command=stream)

####### submenu1<-----------------------


###main


# path = "42.jpg"

# logo = ImageTk.PhotoImage(Image.open(path))
# panel = tk.Label(root, image = logo)
# panel.pack(side = "top", fill = "both", expand = "yes")
# root.configure(background = "black")


# canv = Canvas(root, width=80, height=80, bg='black')
# canv.grid(row=2, column=3)

# img = PhotoImage(file="Logo.jpg")
# canv.create_image(20,20, anchor=NW, image=img)
# logo = PhotoImage(file = "Logo.png")

# main = Label(root,bg = 'BLACK')


##main.pack(fill = X)


mainloop()
