import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import sqlite3 # library untuk database
import random # untuk generate angka random
import time # untuk mengambil current time



# ---------------------------------------------------------------------------------------------------------------------------------------
# CONFIG DATABASE
# ---------------------------------------------------------------------------------------------------------------------------------------

# membuat koneksi ke database
conn = sqlite3.connect('scheduling.db')

c = conn.cursor() # membuat cursor

def buka_koneksi():
    # membuat koneksi ke database
    conn = sqlite3.connect('scheduling.db')
    # membuat cursor
    c = conn.cursor()
    
    return conn, c

# ---------------------------------------------------------------------------------------------------------------------------------------
# FUNCTION TO GENERATE DATA FROM DATABASE
# ---------------------------------------------------------------------------------------------------------------------------------------

def load_guru(): # get data guru
    conn, c = buka_koneksi()
    c.execute("SELECT nama from tb_guru ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Nama Guru'])

def load_mapel(): # get data mapel
    conn, c = buka_koneksi()
    c.execute("SELECT nama_mapel from tb_mapel ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Mata Pelajaran'])

def load_kelas(): # get data kelas
    conn, c = buka_koneksi()
    c.execute("SELECT nama_kelas from tb_kelas ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Kelas'])

def load_hari(): # get data hari
    conn, c = buka_koneksi()
    c.execute("SELECT hari from tb_hari ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Hari'])

def load_jam(): # get data jam
    conn, c = buka_koneksi()
    c.execute("SELECT waktu from tb_jam ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Waktu'])

# ---------------------------------------------------------------------------------------------------------------------------------------
# GET DATA FROM DB / INISIALISASI VARIABEL YANG DIBUTUHKAN
# ---------------------------------------------------------------------------------------------------------------------------------------

data_guru = load_guru()
data_mapel = load_mapel()
data_kelas = load_kelas()
data_hari = load_hari()
data_jam = load_jam()
# load data dari db -> pandas dataframe

# convert df to list
data_guru = data_guru['Nama Guru'].tolist()
data_mapel = data_mapel['Mata Pelajaran'].tolist()
data_kelas = data_kelas['Kelas'].tolist()
data_hari = data_hari['Hari'].tolist()
data_jam = data_jam['Waktu'].tolist()

n_IPA = 14 # jumlah kelas IPA
n_IPS = 10 # jumlah kelas IPS
n_kelas = n_IPA + n_IPS # jumlah kelas
n_sesi = (10*4) + 7 # senin-kamis = 10 sesi dan jumat 7 sesi
hard_bc = 0.0350

# rule mapel

# mapel untuk ipa ips
mapel_ipa = [0,1,2,3,4,6,7,8,9,10,11,13,16,17,18,20,21,22] # kelas ipa
mapel_ips = [0,1,2,4,5,6,7,8,12,13,14,15,16,19,20,21,22,23] # kelas ips

# waktu sesi setiap kelas
waktu_sesi_ipa = [
    [3, 2, 4, 3, 2, 0, 2, 3, 2, 3, 3, 3, 0, 2, 0, 0, 0, 3, 3, 0, 4, 2, 2, 0], # X IPA
    [3, 2, 4, 4, 2, 0, 2, 3, 2, 4, 4, 4, 0, 2, 0, 0, 4, 0, 0, 0, 4, 2, 0, 0], # XI IPA
    [3, 2, 4, 4, 2, 0, 2, 3, 2, 4, 4, 4, 0, 2, 0, 0, 4, 0, 0, 0, 4, 2, 0, 0] # XII IPA
# id 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23
]

waktu_sesi_ips = [
    [3, 2, 4, 0, 2, 3, 2, 3, 2, 0, 0, 0, 3, 2, 3, 3, 0, 0, 0, 3, 4, 2, 2, 3], # X IPS
    [3, 2, 4, 0, 2, 0, 2, 3, 2, 0, 0, 0, 4, 2, 4, 4, 4, 0, 0, 0, 4, 2, 0, 4], # XI IPS
    [3, 2, 4, 0, 2, 0, 2, 3, 2, 0, 0, 0, 4, 2, 4, 4, 4, 0, 0, 0, 4, 2, 0, 4] # XII IPS
# id 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23
]

guru_pengampu = [
    [5, 38], # Pendidikan Agama dan Budi Pekerti (PAI)
    [0, 50, 51], # PPKN
    [3, 4, 32, 35], # Bahasa Indonesia
    [8, 24, 45], # Matematika
    [6, 30], # Bahasa Inggris
    [19], # Biologi Lintas Minat
    [15, 46, 49], # Seni Budaya
    [12, 27, 44, 48, 52], # Penjaskes
    [31, 39, 40], # Prakarya
    [13, 21], # Biologi
    [17, 18], # Kimia
    [9, 25, 33], # Fisika
    [14, 26], # Geografi
    [29, 37], # Sejarah Indonesia
    [1], # Sosiologi
    [11, 23], # Ekonomi
    [2, 7], # Bahasa dan Sastra Inggris
    [16], # Ekonomi Lintas Minat
    [20], # Sosiologi Lintas Minat
    [22], # Fisika Lintas Minat
    [10, 34, 47], # Matematika Umum
    [41, 42, 43], # Bahasa Madura
    [28], # TIK
    [36], # Sejarah Peminatan
]

# ---------------------------------------------------------------------------------------------------------------------------------------
# KUMPULAN FUNCTION
# ---------------------------------------------------------------------------------------------------------------------------------------

# fungsi untuk menampilkan teks
def printing_text(teks_1, teks_2):
    col1, col2 = st.columns([1,3])
    with col1:
        st.markdown(teks_1)
    with col2:
        st.markdown(f'`{teks_2}`')

# fungsi untuk menampilkan teks menggunakan streamlit.info
def printing_info(teks_1, teks_2):
    col1, col2, col3 = st.columns([0.5,3,0.5])
    with col1:
        st.markdown(teks_1)
    with col2:
        st.info(teks_2)
    with col3:
        st.markdown(teks_1)

# fungsi untuk memberikan space kosong antar section
def spaces():
    st.markdown('##### ')

# function untuk membuat kromosom
def make_kromosom():
    kromosom = list()
    for i in range(n_kelas):
        # identifikasi kelas, x ipa 4, x ips 3, xi ipa 5, xi ips 3, xii ipa 5, xii ips 4
        kelas = 0 if i < 4 else 1 if i < 9 else 2 if i < 14 else 0 if i < 17 else 1 if i < 20 else 2
        gen = [[] for i in range(n_sesi)] # membuat sesi dari list kosong sebanyak panjang sesi (47)
        gen[0] = ['Upacara',''] # untuk mapel pertama selalu upacara

        if i < n_IPA: # untuk ke 14 kelas ipa
            daftar_mapel = mapel_ipa.copy() # membuat tampungan daftar mapel ipa
            random.shuffle(daftar_mapel) # list tampungan yg dibuat di acak agar saat diambil tetap bersifat random
            increment = 1 # untuk cursor pengisian di setiap sesi

            for mapel in daftar_mapel: # list tampungan yg di acak, digunakan sebagai refrensi pengambilan mapel
                if waktu_sesi_ipa[kelas][mapel] > 0: # cek rule sesi dari mapel yg diambil (panjang sesi)
                    id_guru = random.choice(guru_pengampu[mapel]) # untuk mapel yg diambil, ambil guru pengampu secara random
                    # perulangan untuk memasukan mapel ke dalam kromosom / jadwal yg akan dibuat
                    for sesi_mapel in range(waktu_sesi_ipa[kelas][mapel]):
                        
                        # mulai pengisian mapel ke dalam sesi jadwal setiap kelas
                        if increment <= len(gen):
                            if gen[increment] == []:
                                gen[increment] = [data_mapel[mapel], id_guru]
                            else:
                                gen[increment + 1] = [data_mapel[mapel], id_guru]
                        increment += 1 # jangan lupa incrementnya
                        
        else: # disini untuk kelas ips yg jumlah nya 10 kelas kalo ga salah
            daftar_mapel = mapel_ips.copy() # membuat tampungan daftar mapel ips
            random.shuffle(daftar_mapel) # list tampungan yg dibuat di acak agar saat diambil tetap bersifat random
            increment = 1 # untuk cursor pengisian di setiap sesi

            for mapel in daftar_mapel: # list tampungan yg di acak, digunakan sebagai refrensi pengambilan mapel
                if waktu_sesi_ips[kelas][mapel] > 0: # cek rule sesi dari mapel yg diambil (panjang sesi)
                    id_guru = random.choice(guru_pengampu[mapel]) # untuk mapel yg diambil, ambil guru pengampu secara random
                    # perulangan untuk memasukan mapel ke dalam kromosom / jadwal yg akan dibuat
                    for sesi_mapel in range(waktu_sesi_ips[kelas][mapel]):
                        
                        # mulai pengisian mapel ke dalam sesi jadwal setiap kelas
                        if increment <= len(gen):
                            if gen[increment] == []:
                                gen[increment] = [data_mapel[mapel], id_guru]
                            else:
                                gen[increment + 1] = [data_mapel[mapel], id_guru]
                        increment += 1 # jangan lupa incrementnya

        indices_to_move = []
        for i, item in enumerate(gen):
            if item[0] == 'Penjaskes':
                indices_to_move.append(i)

        if indices_to_move[0] == 1 or indices_to_move[0] == 10 or indices_to_move[0] == 20 or indices_to_move[0] == 30 or indices_to_move[0] == 40:
            pass
        else:
            sesi_penjas = [1, 10, 20, 30, 40]
            rand_sesi = random.choice(sesi_penjas)
            # Pindahkan sesi mata pelajaran 'Penjaskes' ke indeks sebelumnya
            gen[indices_to_move[0]], gen[rand_sesi] = gen[rand_sesi], gen[indices_to_move[0]]
            gen[indices_to_move[1]], gen[rand_sesi + 1] = gen[rand_sesi + 1], gen[indices_to_move[1]]
            gen[indices_to_move[2]], gen[rand_sesi + 2] = gen[rand_sesi + 2], gen[indices_to_move[2]]

        # setiap perulangan, baik itu untuk jadwal ipa ataupun ips
        # jangan lupa disimpan kedalam list tampungan yg namanya kromosom
        kromosom.append(gen)
    return kromosom # kalo sudah, di return yaak

# function untuk mutasi
def mutasi(i, mapel_ipa, mapel_ips, waktu_sesi_ipa, waktu_sesi_ips, data_mapel, guru_pengampu):
    # identifikasi kelas, x ipa 4, x ips 3, xi ipa 5, xi ips 3, xii ipa 5, xii ips 4
    kelas = 0 if i < 4 else 1 if i < 9 else 2 if i < 14 else 0 if i < 17 else 1 if i < 20 else 2

    if i < n_IPA: # untuk ke 14 kelas ipa
        gen = [[] for i in range(n_sesi)] # membuat sesi dari list kosong sebanyak panjang sesi (47)
        gen[0] = ['Upacara',''] # untuk mapel pertama selalu upacara
        
        daftar_mapel = mapel_ipa.copy() # membuat tampungan daftar mapel ipa
        random.shuffle(daftar_mapel) # list tampungan yg dibuat di acak agar saat diambil tetap bersifat random
        increment = 1 # untuk cursor pengisian di setiap sesi

        for mapel in daftar_mapel: # list tampungan yg di acak, digunakan sebagai refrensi pengambilan mapel
            if waktu_sesi_ipa[kelas][mapel] > 0: # cek rule sesi dari mapel yg diambil (panjang sesi)
                id_guru = random.choice(guru_pengampu[mapel]) # untuk mapel yg diambil, ambil guru pengampu secara random
                # perulangan untuk memasukan mapel ke dalam kromosom / jadwal yg akan dibuat
                for sesi_mapel in range(waktu_sesi_ipa[kelas][mapel]):
                    
                    # mulai pengisian mapel ke dalam sesi jadwal setiap kelas
                    if increment <= len(gen):
                        if gen[increment] == []:
                            gen[increment] = [data_mapel[mapel], id_guru]
                        else:
                            gen[increment + 1] = [data_mapel[mapel], id_guru]
                    increment += 1 # jangan lupa incrementnya
                                        
    else: # disini untuk kelas ips yg jumlah nya 10 kelas kalo ga salah
        gen = [[] for i in range(n_sesi)] # membuat sesi dari list kosong sebanyak panjang sesi (47)
        gen[0] = ['Upacara',''] # untuk mapel pertama selalu upacara
        
        daftar_mapel = mapel_ips.copy() # membuat tampungan daftar mapel ips
        random.shuffle(daftar_mapel) # list tampungan yg dibuat di acak agar saat diambil tetap bersifat random
        increment = 1 # untuk cursor pengisian di setiap sesi

        for mapel in daftar_mapel: # list tampungan yg di acak, digunakan sebagai refrensi pengambilan mapel
            if waktu_sesi_ips[kelas][mapel] > 0: # cek rule sesi dari mapel yg diambil (panjang sesi)
                id_guru = random.choice(guru_pengampu[mapel]) # untuk mapel yg diambil, ambil guru pengampu secara random
                # perulangan untuk memasukan mapel ke dalam kromosom / jadwal yg akan dibuat
                for sesi_mapel in range(waktu_sesi_ips[kelas][mapel]):
                    
                    # mulai pengisian mapel ke dalam sesi jadwal setiap kelas
                    if increment <= len(gen):
                        if gen[increment] == []:
                            gen[increment] = [data_mapel[mapel], id_guru]
                        else:
                            gen[increment + 1] = [data_mapel[mapel], id_guru]
                    increment += 1 # jangan lupa incrementnya

    indices_to_move = []
    for i, item in enumerate(gen):
        if item[0] == 'Penjaskes':
            indices_to_move.append(i)

    if indices_to_move[0] == 1 or indices_to_move[0] == 10 or indices_to_move[0] == 20 or indices_to_move[0] == 30 or indices_to_move[0] == 40:
        pass
    else:
        sesi_penjas = [1, 10, 20, 30, 40]
        rand_sesi = random.choice(sesi_penjas)
        # Pindahkan sesi mata pelajaran 'Penjaskes' ke indeks sebelumnya
        gen[indices_to_move[0]], gen[rand_sesi] = gen[rand_sesi], gen[indices_to_move[0]]
        gen[indices_to_move[1]], gen[rand_sesi + 1] = gen[rand_sesi + 1], gen[indices_to_move[1]]
        gen[indices_to_move[2]], gen[rand_sesi + 2] = gen[rand_sesi + 2], gen[indices_to_move[2]]

    return gen # kalo sudah, di return yaak

# rule constrain
# dalam 1 waktu yg sama guru tidak boleh mengajar lebih dari 1 sesi mata pelajaran
def rule1(kromosom):
    temp = list() # buat list untuk tampungan
    for i in range(len(kromosom[0])): # terus cek banyak nya kelas
        res = list() # buat list lagi untuk tampungan
        for j in range(len(kromosom)): # perulangan untuk setiap kromosom (sebanyak popsize harusnya bakal ada 10)
            # mengambil anggota terakhir (indeks -1) dari list yang berada pada indeks ke-0
            # gampangannya, disini kita ingin mengambil id si guru
            res.append(kromosom[j][i][-1])
        temp.append(res) # kalo udah dapet tuh list guru-gurunya, masukin deh ke temp
        # kenapa kok dimasukin ke temp? karna gini, kan total ada 24 kelas
        # nah si res hanya menampung total 47 sesi tadi untuk 1 kelas saja
        # karna kita ingin tau keseluruhan guru yg mengajar di 24 kelas tadi
        # maka setiap res akan di tampung dulu di temp, nah skrng isi dari temp adalah id guru sebanyak 47 sesi dalam 24 kelas

    hasil = int() # buat 0 dulu yaa
    for i in range(len(temp)): # cek panjang list temp, harusnya bakal ada 24 (mewakili total kelas kita)
        # disini branching untuk menghindari index ke 0, karna index 0 sudah pasti ga ada gurunya
        # kan ada upacara, jadi tiap senin mereka upacara gitu tuh
        if i != 0:
            id_guru = list() # buat list yaa untuk menampung id setiap guru nantinya
            for ind in temp[i]: # sekarang cek untuk setiap sesi di seluruh kelas
                # nah kalo ga ditemukan id guru dalam list yg udah dibuat tampungan id guru tadi
                if ind not in id_guru:
                    id_guru.append(ind) # masukin tuh id guru nya ke list tampungan tadi
            for j in id_guru: # disini perulangan untuk ngecek id guru yaa
                # terus cek, kalo seumpama dalam satu sesi yg sama (meski beda kelas)
                # kalo id guru itu tadi muncul lebih dari 1, berarti kan maruk tuh gurunya
                if temp[i].count(j) > 1:
                    hasil += hard_bc # nah kalo udah maruk, kasih SP deh, berupa penambahan bobot constrainnya 0.001

    return hasil # jangan lupa di return nilai constrainnya

# rule constrain
# setiap guru mengajar maksimal 36 jam
def rule2(kromosom):
    temp = list() # buat list untuk tampungan
    for i in range(len(kromosom[0])): # terus cek banyak nya kelas
        res = list() # buat list lagi untuk tampungan
        for j in range(len(kromosom)): # perulangan untuk setiap kromosom (sebanyak popsize harusnya bakal ada 10)
            # mengambil anggota terakhir (indeks -1) dari list yang berada pada indeks ke-0
            # gampangannya, disini kita ingin mengambil id si guru
            res.append(kromosom[j][i][-1])
        temp.append(res) # kalo udah dapet tuh list guru-gurunya, masukin deh ke temp
        # kenapa kok dimasukin ke temp? karna gini, kan total ada 24 kelas
        # nah si res hanya menampung total 47 sesi tadi untuk 1 kelas saja
        # karna kita ingin tau keseluruhan guru yg mengajar di 24 kelas tadi
        # maka setiap res akan di tampung dulu di temp, nah skrng isi dari temp adalah id guru sebanyak 47 sesi dalam 24 kelas

    hasil = int() # buat 0 dulu yaa
    for i in range(len(temp)): # cek panjang list temp, harusnya bakal ada 24 (mewakili total kelas kita)
        # disini branching untuk menghindari index ke 0, karna index 0 sudah pasti ga ada gurunya
        # kan ada upacara, jadi tiap senin mereka upacara gitu tuh
        res = int()
        for j in range(len(kromosom)):
            res += (kromosom[j].count(i))
        if res > 36:
            hasil += hard_bc

    return hasil # jangan lupa di return nilai constrainnya

# function untuk menghitung nilai fitness
def func_fitness(populasi):
    fitness = list() # buat list untuk menampung nilai fitness dari semua gen (10 gen sesuai popsize)
    for i in range(len(populasi)): # perulangan untuk setiap gen
        nilai_fitness = 1/(1 + rule1(populasi[i]) + rule2(populasi[i])) # hitung nilai fitness setiap gen pake fungsi rule tadi
        fitness.append(nilai_fitness) # masukin nilai fitness yg udah di hitung ke list tampungan tadi
    return fitness # terus di return lah

# nah di sini main sistem nya
# jadi ku buat func untuk memudahkan proses running program
# juga biar gampang aja ngecek waktu komputasi nya

def penjadwalan(cr, mr, popsize, max_iter):
    populasi_awal = list() # buat list kosong buat nampung populasi awal
    for i in range(popsize): # buat kromosom sebanya gen / nilai popsize
        populasi_awal.append(make_kromosom()) # setiap gen nya masukin ke populasi awal
    populasi = populasi_awal.copy() # terus populasi awal tadi di gandakan dulu ya, nanti soalnya dibutuhkan

    generasi = 1 # disini log generasi biar kita tahu berapa generasi yg udah di buat
    best = int() # terus ini variabel buat ngecek fitness disetiap generasi
    best_fitness = int() # nah ini untuk nyimpen nilai fitness dari generasi terbaik
    total_fitness = 0

    while best != 1 and generasi <= max_iter: # oke skrang jalankan GA sebanyak max_iter yang diinginkan

        temp = func_fitness(populasi) # nah disini kita hitung dulu nilai fitness dari populasi awal tadi
        sorting = temp.copy() # terus di copy dulu
        sorting.sort() # kalo udah urutkan nilai fitness duplikat dari populasi awal tadi

        # di sini kita hitung, kita mau buat anak berapa
        # eh maaf salah, maksutnya kita hitung, berapa banyak ortu yg boleh mantab mantab
        offspringcross = int(popsize * cr) # 4
        cross = list() # buat list kosong dulu yaa

        for i in sorting[offspringcross:]: # terus ambil ortu ortu terpilih tadi
            cross.append(populasi[temp.index(i)].copy()) # nah ortu nya masukin ke list
            # jadi disini kita isolasi mereka biar nyaman pas mantab mantab

        ortu = list() # buat list kosong lagi
        for i in cross:
            res = random.randrange(0, len(populasi_awal[0])) # ambil ortu dari populasi awal secara random
            ortu.append(res) # masukin ke dalam ortu

        anak = list() # sekarng buat list untuk nampung hasil perbuatan si ortu
        for i in range(len(cross)): # perulangan sebanyak ortu terpilih
            cross_ = cross.copy() # di duplikat dulu list yg isinya ortu terpilih
            born = cross_[i].copy() # terus untuk setiap gen dari ortu tampung dalam born

            # di sini kita lakukan proses crossover antar 2 ortu dengan urutan index pertama
            # sampai di crossover kembali ke index pertama
            if i != len(ortu) - 1:
                idx = i + 1
                ortu_ = cross_[i + 1].copy()
            else:
                idx = 0
                ortu_ = cross_[0].copy()
            born_ = ortu_[ortu[i]].copy()
            born[ortu[i]] = born_ # hasil dari proses crossover ini akan menghasilkan anak yg baru lahir
            # kita kasih nama born aja yaa

        # kita lakukan mutasi dengan tujuan untk mengembalikan kerusakan materi gen selama proses crossover tadi
        for i in range(len(born)):
            # disini, peluang untuk mutasi di notasikan dengan angka random dari 0-10 | 9/10 = 0.9 < 0.8
            # angka random tadi harus di bagi 10 dan dibandingkan dengan nilai mr
            # kalo lebih besar mr maka mutasi boleh dilakukan, kalo sebliknya yaa jangan harap mutasi lahh
            if random.randrange(0, 11)/10 < mr: # mr = mutasi rate
                # panggil func mutasi
                born[i] = mutasi(i, mapel_ipa, mapel_ips, waktu_sesi_ipa, waktu_sesi_ips, data_mapel, guru_pengampu).copy()
                break
        anak.append(born) # nah hasil akhir dari crossover dan mutasi, masukin ke list anak
        # karna udah gede dan yaa berhak untuk dianggap sbg suatu individu dalam populasi

        for i in range(len(anak)): # untuk setiap anak
            # cek nilai fitnessnya, apakah lebih besar dari populasi ortnya
            if func_fitness([populasi[sorting.index(sorting[i])]])[0] <= func_fitness([anak[i]])[0]:
                # kalau ternyata lebih bagus si anak
                # berarti ortu ketinggalan zaman dan kita gantikan dengan si anak
                populasi[temp.index(sorting[i])] = anak[i].copy()

        # disini kita ambil nilai fitness nya si anak
        best = func_fitness([populasi[i]])[0]
        print('Generasi %d' % generasi) # print info generasi
        print('Fitness =',best) # print info generasi
        total_fitness += best

        if best_fitness < best: # disini branching buat kita simpen individu terbaik
            best_fitness = best # ambil nilai fitnessnya
            generasi_ke = generasi # cari tahu dia generasi ke berapa
            populasi_final = populasi # trus comot juga individu tadi

        generasi += 1 # increment info generasi
        
    return total_fitness, best_fitness, generasi_ke, populasi_final # return info info tadi

def buat_jadwal(jadwal, kelas):
    jadwal_kelas = []
    for jam in range(len(jadwal[kelas])):
        if jadwal[kelas][jam][1] == '':
            value_sesi = f'{jadwal[kelas][jam][0]}'
        else:
            value_sesi = f'{jadwal[kelas][jam][0]} - {data_guru[jadwal[kelas][jam][1]]}'
        jadwal_kelas.append(value_sesi)
        
    return jadwal_kelas

st.set_page_config(
    page_title="Optimasi Penjadwalan Mata Pelajaran Menggunakan Genetic Algoritm",
    page_icon='smator.png',
    layout='wide',
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

with st.container():
    with st.sidebar:
        selected = option_menu(
        #Ganti foto di navbar
        st.write("""<h3 style = "text-align: center;"><img src="data:image/jpeg;base64,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" width="100" height="90"><br>OPTIMASI PENJADWALAN MATA PELAJARAN MENGGUNAKAN <p>GENETIC ALGORITM</p></h3>""",unsafe_allow_html=True), 
        ["Home", "Data", "Penjadwalan"], 
            icons=['house', 'file-earmark-font', 'gear'], menu_icon="cast", default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#1E90FF"},#ini untuk ganti warna navbarnya 
                "icon": {"color": "white", "font-size": "18px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "color":"white"},
                "nav-link-selected":{"background-color": "#FF4B4B"}#ini untuk ganti warna navbarnya 
            }
        )

    if selected == "Home":
        
        # tampilkan judul sistem
        st.write('''
        # Optimasi Penjadwalan Mata Pelajaran
        ''')

        # inisialisasi informasi penelitian
        info = '''
        - Penerapan yang dilakukan menggunakan metode **Genetic Algorithm (GA)**
        - Penelitian dilakukan dengan studi kasus di **SMA Negeri 1 Torjun, Sampang**
        '''

        # tampilkan informasi yg dibuat ke dalam sistem
        st.info(info)

    elif selected == "Data":
        # navigation point untuk dataset section
        st.markdown('''
        ## **Data**
        ''')
        pilih_data = st.selectbox('Lihat Data', ['Guru', 'Mata Pelajaran', 'Kelas'], index= 0)
        if pilih_data == 'Guru':
            # membuat daftar mapel yg di ampu oleh setiap guru
            pengampu = ['' for i in range(len(data_guru))]
            for indices, data in enumerate (guru_pengampu):
                for guru in data:
                    pengampu[guru] = data_mapel[indices]

            # membuat dataframe untuk data guru
            df_guru = pd.DataFrame(
                {
                    'Nama Guru' : data_guru,
                    'Bidang Studi' : pengampu
                }
            )
            # tampilkan dataframe
            st.dataframe(
                df_guru,
                use_container_width=True,
            )
        elif pilih_data == 'Mata Pelajaran':
            # buat dataframe untuk data mapel
            no_mapel = [i+1 for i in range(len(data_mapel))]
            df_mapel = pd.DataFrame(
                {
                    'No' : no_mapel,
                    'Nama Mata Pelajaran' : data_mapel
                }
            )
            # tampilkan dataframe
            st.dataframe(
                df_mapel,
                use_container_width=True
            )
        elif pilih_data == 'Kelas':
            # buat dataframe untuk data kelas
            no_kelas = [i+1 for i in range(len(data_kelas))]
            df_kelas = pd.DataFrame(
                {
                    'No' : no_kelas,
                    'Kelas' : data_kelas
                }
            )
            # tampilkan dataframe
            st.dataframe(
                df_kelas,
                use_container_width=True
            )
        
    elif selected == "Penjadwalan":

        # navigation point untuk dataset section
        st.markdown('''
        ## **Penjadwalan Mata Pelajaran**
        ''')

        # try:
        # # layouting kolom untuk data section
        # col_jadwal = st.columns([0.4,0.1,2])

        # with col_jadwal[0]: # layout bagian kiri
        # input number widget untuk nilai cr
        value_cr = st.number_input('**cr** value', min_value= 0.1, max_value= 0.9, value= 0.1, step= 0.1, key= 'cr value',format="%.1f")

        # input number widget untuk nilai mr
        value_mr = st.number_input('**mr** value', min_value= 0.1, max_value= 0.9, value= 0.1, step= 0.1, key= 'mr value',format="%.1f")

        # input number widget untuk nilai popsize
        value_pop = st.number_input('**popsize** value', min_value= 10, max_value= 100, value= 10, step= 10, key= 'pop value')

        # input number widget untuk nilai n_generasi
        value_gen = st.number_input('**jumlah generasi** value', min_value= 100, max_value= 5000, value= 100, step= 100, key= 'generasi value')

        spaces() # memberikan space kosong
        # button train model
        button_apply = st.button('Apply')

        # with col_jadwal[2]: # layout bagian kanan
        if button_apply:
            # Waktu mulai
            start_time = time.time()

            with st.spinner('Wait for it...'):
                # penjadwalan GA
                total_fitness, best_fitness, generasi_ke, populasi_final = penjadwalan(value_cr, value_mr, value_pop, value_gen)

            # Waktu selesai
            end_time = time.time()

            tr_duration = end_time - start_time
            hours = tr_duration // 3600
            minutes = (tr_duration - (hours * 3600)) // 60
            seconds = tr_duration - ((hours * 3600) + (minutes * 60))


            for i, fitness in enumerate(func_fitness(populasi_final)):
                if best_fitness == fitness:
                    jadwal_GA = populasi_final[i]

            # jadwal
            sesi = [i % 10 + 1 for i in range(n_sesi)]
            sesi[40:] = [i % 7 + 1 for i in range(7)]

            jadwal = jadwal_GA.copy()

            for kelas in range(len(jadwal)):
                if kelas == 0:
                    x_ipa_1 = buat_jadwal(jadwal, kelas)
                elif kelas == 1:
                    x_ipa_2 = buat_jadwal(jadwal, kelas)
                elif kelas == 2:
                    x_ipa_3 = buat_jadwal(jadwal, kelas)
                elif kelas == 3:
                    x_ipa_4 = buat_jadwal(jadwal, kelas)
                elif kelas == 4:
                    xi_ipa_1 = buat_jadwal(jadwal, kelas)
                elif kelas == 5:
                    xi_ipa_2 = buat_jadwal(jadwal, kelas)
                elif kelas == 6:
                    xi_ipa_3 = buat_jadwal(jadwal, kelas)
                elif kelas == 7:
                    xi_ipa_4 = buat_jadwal(jadwal, kelas)
                elif kelas == 8:
                    xi_ipa_5 = buat_jadwal(jadwal, kelas)
                elif kelas == 9:
                    xii_ipa_1 = buat_jadwal(jadwal, kelas)
                elif kelas == 10:
                    xii_ipa_2 = buat_jadwal(jadwal, kelas)
                elif kelas == 11:
                    xii_ipa_3 = buat_jadwal(jadwal, kelas)
                elif kelas == 12:
                    xii_ipa_4 = buat_jadwal(jadwal, kelas)
                elif kelas == 13:
                    xii_ipa_5 = buat_jadwal(jadwal, kelas)
                elif kelas == 14:
                    x_ips_5 = buat_jadwal(jadwal, kelas)
                elif kelas == 15:
                    x_ips_6 = buat_jadwal(jadwal, kelas)
                elif kelas == 16:
                    x_ips_7 = buat_jadwal(jadwal, kelas)
                elif kelas == 17:
                    xi_ips_6 = buat_jadwal(jadwal, kelas)
                elif kelas == 18:
                    xi_ips_7 = buat_jadwal(jadwal, kelas)
                elif kelas == 19:
                    xi_ips_8 = buat_jadwal(jadwal, kelas)
                elif kelas == 20:
                    xii_ips_6 = buat_jadwal(jadwal, kelas)
                elif kelas == 21:
                    xii_ips_7 = buat_jadwal(jadwal, kelas)
                elif kelas == 22:
                    xii_ips_8 = buat_jadwal(jadwal, kelas)
                elif kelas == 23:
                    xii_ips_9 = buat_jadwal(jadwal, kelas)
            
            dict_jadwal = {
                'Hari' : '',
                'Sesi' : sesi,
                'X IPA 1' : x_ipa_1,
                'X IPA 2' : x_ipa_2,
                'X IPA 3' : x_ipa_3,
                'X IPA 4' : x_ipa_4,
                'XI IPA 1' : xi_ipa_1,
                'XI IPA 2' : xi_ipa_2,
                'XI IPA 3' : xi_ipa_3,
                'XI IPA 4' : xi_ipa_4,
                'XI IPA 5' : xi_ipa_5,
                'XII IPA 1' : xii_ipa_1,
                'XII IPA 2' : xii_ipa_2,
                'XII IPA 3' : xii_ipa_3,
                'XII IPA 4' : xii_ipa_4,
                'XII IPA 5' : xii_ipa_5,
                'X IPS 5' : x_ips_5,
                'X IPS 6' : x_ips_6,
                'X IPS 7' : x_ips_7,
                'XI IPS 6' : xi_ips_6,
                'XI IPS 7' : xi_ips_7,
                'XI IPS 8' : xi_ips_8,
                'XII IPS 6' : xii_ips_6,
                'XII IPS 7' : xii_ips_7,
                'XII IPS 8' : xii_ips_8,
                'XII IPS 9' : xii_ips_9,
            }

            df_jadwal = pd.DataFrame(dict_jadwal)
            
            temp = 0
            for indices, jam in enumerate (sesi):
                if jam == 1:
                    df_jadwal['Hari'][indices] = data_hari[temp]
                    temp += 1
                else:
                    df_jadwal['Hari'][indices] = ' '

            st.subheader("Data Jadwal")
            st.dataframe(df_jadwal, use_container_width=True)
            df_jadwal.to_csv('Penjadwalan GA.csv', index=False)

            st.subheader("Hasil Percobaan")
            #Code buat ngelakuin percobaan
            cr = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
            mr = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
            popsize = [10]
            generasi = [20]
            percobaan = []
            for a in range(len(cr)):
                for i in range(len(mr)) :
                    for u in range(len(popsize)):
                        for e in range(len(generasi)):
                            hasil = []
                            start_time = time.time()
                            total_fitness, best_fitness, generasi_ke, populasi_final = penjadwalan(cr[a], mr[i], popsize[u], generasi[e])
                            end_time = time.time()
                            tr_duration = end_time - start_time
                            hours = tr_duration // 3600
                            minutes = (tr_duration - (hours * 3600)) // 60
                            seconds = tr_duration - ((hours * 3600) + (minutes * 60))
                            msg = f'{seconds:4.2f} detik'
                            hasil.append(cr[a])
                            hasil.append(mr[i])
                            hasil.append(popsize[u])
                            hasil.append(generasi[e])
                            hasil.append(best_fitness)
                            hasil.append(total_fitness/generasi[e])
                            hasil.append(msg)
                            percobaan.append(hasil)
            
            percobaan_sistem = pd.DataFrame(percobaan, columns=['Cr','Mr','Popsize','Generasi','Best Fitness','Average Fitness','msg'])
            st.write(percobaan_sistem)

            percobaan_sistem.to_csv('percobaan.csv')
            df_percobaan = pd.read_csv('percobaan1.csv')
            df_percobaan_1 = df_percobaan.drop(columns=["Cr","Mr"]) 
            df_percobaan_cr = df_percobaan["Cr"].map('{:.1f}'.format)
            df_percobaan_mr = df_percobaan["Mr"].map('{:.1f}'.format)

            df_percobaan_asli = pd.concat([df_percobaan_cr,df_percobaan_mr,df_percobaan_1], axis=1) 
            st.dataframe(df_percobaan_asli,use_container_width=True)

            #Grafik Hasil Percobaan
            ##Cr 0.1
            st.write("#### Cr 0.1")
            df_01 = df_percobaan_asli[df_percobaan_asli["Cr"] == "0.1"]
            st.dataframe(df_01,use_container_width=True)
            st.line_chart(data=df_01[["Cr","Mr","Average Fitness"]], x="Mr", y="Average Fitness", width=0, height=0, use_container_width=True)

            ##Cr 0.2
            st.write("#### Cr 0.2")
            df_02 = df_percobaan_asli[df_percobaan_asli["Cr"] == "0.2"]
            st.dataframe(df_02,use_container_width=True)
            st.line_chart(data=df_02[["Cr","Mr","Average Fitness"]], x="Mr", y="Average Fitness", width=0, height=0, use_container_width=True)

            ##Cr 0.3
            st.write("#### Cr 0.3")
            df_03 = df_percobaan_asli[df_percobaan_asli["Cr"] == "0.3"]
            st.dataframe(df_03,use_container_width=True)
            st.line_chart(data=df_03[["Cr","Mr","Average Fitness"]], x="Mr", y="Average Fitness", width=0, height=0, use_container_width=True)
            
            ##Cr 0.4
            st.write("#### Cr 0.4")
            df_04 = df_percobaan_asli[df_percobaan_asli["Cr"] == "0.4"]
            st.dataframe(df_04,use_container_width=True)
            st.line_chart(data=df_04[["Cr","Mr","Average Fitness"]], x="Mr", y="Average Fitness", width=0, height=0, use_container_width=True)

            ##Cr 0.5
            st.write("#### Cr 0.5")
            df_05 = df_percobaan_asli[df_percobaan_asli["Cr"] == "0.5"]
            st.dataframe(df_05,use_container_width=True)
            st.line_chart(data=df_05[["Cr","Mr","Average Fitness"]], x="Mr", y="Average Fitness", width=0, height=0, use_container_width=True)

            ##Cr 0.6
            st.write("#### Cr 0.6")
            df_06 = df_percobaan_asli[df_percobaan_asli["Cr"] == "0.6"]
            st.dataframe(df_06,use_container_width=True)
            st.line_chart(data=df_06[["Cr","Mr","Average Fitness"]], x="Mr", y="Average Fitness", width=0, height=0, use_container_width=True)

            ##Cr 0.7
            st.write("#### Cr 0.7")
            df_07 = df_percobaan_asli[df_percobaan_asli["Cr"] == "0.7"]
            st.dataframe(df_07,use_container_width=True)
            st.line_chart(data=df_07[["Cr","Mr","Average Fitness"]], x="Mr", y="Average Fitness", width=0, height=0, use_container_width=True)

            ##Cr 0.8
            st.write("#### Cr 0.8")
            df_08 = df_percobaan_asli[df_percobaan_asli["Cr"] == "0.8"]
            st.dataframe(df_08,use_container_width=True)
            st.line_chart(data=df_08[["Cr","Mr","Average Fitness"]], x="Mr", y="Average Fitness", width=0, height=0, use_container_width=True)

            ##Cr 0.9
            st.write("#### Cr 0.9")
            df_09 = df_percobaan_asli[df_percobaan_asli["Cr"] == "0.9"]
            st.dataframe(df_09,use_container_width=True)
            st.line_chart(data=df_09[["Cr","Mr","Average Fitness"]], x="Mr", y="Average Fitness", width=0, height=0, use_container_width=True)


            st.subheader("Hasil Implementasi")
            printing_text('Cr', '%.1f' % value_cr)
            printing_text('Mr', '%.1f' % value_mr)
            printing_text('Nilai Rata-rata Fitness', '%.3f' % (total_fitness/value_gen))
            printing_text('Nilai Fitness terbaik', '%.3f' % best_fitness)
            printing_text('Generasi terbaik', '%d' % generasi_ke)
            msg = f'{str(hours)} jam, {minutes:4.1f} menit, {seconds:4.2f} detik'
            printing_text('Waktu komputasi', msg)

        if not button_apply:
            try:
                read = pd.read_csv('Penjadwalan GA.csv')
                st.dataframe(read, use_container_width=True)
            except:
                pass

        # ---------------------------------------------------------------------------------------------------------------------------------------
        # FOOTER SECTION
        # ---------------------------------------------------------------------------------------------------------------------------------------

        # modifikasi bagian footer menggunakan css
        footer="""
            <style>
                footer{
                    visibility: visible;
                }
                footer:before{
                    content: 'Copyright © 2023, Nailatur Rohmah';
                    display: block;
                }
                .css-17es36v {
                    color: rgba(209, 209, 209, 1);
                }
            </style>
        """
        # tampilkan hasil modifikasi pada footer
        st.markdown(footer, unsafe_allow_html=True)
