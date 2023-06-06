# Oviya Jeyaprakash, 3/7/2023 
# Substitution Ciphers and Genetic Algorithms
# l610

from operator import index
import sys
import re
import random
import math
import string

real_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
n_grams_dict = {}
cipher_fitness_dict = {}

POPULATION_SIZE = 500
NUM_CLONES = 2
TOURNAMENT_SIZE = 30
TOURNAMENT_WIN_PROBABILITY = 0.75
CROSSOVER_LOCATIONS = 4
MUTATION_RATE = 0.9

with open("ngrams.txt") as f:
    for line in f:
        substring, value = line.split(" ")
        n_grams_dict[substring] = value

def make_encoder_alphabet(cipher):
    result_dict = {}
    for i in range(len(cipher)):
        result_dict[real_alphabet[i]] = cipher[i]
    return result_dict

def make_decoder_alphabet(cipher):
    result_dict = {}
    for i in range(len(cipher)):
        result_dict[cipher[i]] = real_alphabet[i]
    return result_dict

def encode(decoded_string, cipher_encoder):
    decoded_string = decoded_string.upper()
    result_string = ""
    for char in decoded_string:
        if char in cipher_encoder:
            result_string += cipher_encoder[char]
        else:
            result_string += char
    return result_string

def decode(encoded_string, cipher_decoder):
    encoded_string = encoded_string.upper()
    result_string = ""
    for char in encoded_string:
        if char in cipher_decoder:
            result_string += cipher_decoder[char]
        else:
            result_string += char
    return result_string

def n_gram_substring(n_value, string):
    result = [string[i:j] for i in range(len(string)) for j in range(i + 1, len(string) + 1) if len(string[i:j]) == n_value]
    return result

def fitness(n_value, encoded_string, cipher):
    if cipher in cipher_fitness_dict:
        return cipher_fitness_dict[cipher]

    cipher_alphabet = make_decoder_alphabet(cipher)
    decoded_string = decode(encoded_string, cipher_alphabet)

    # with open('readme.txt', 'w') as f:
    #     f.write(str(cipher) + ":\n" + decoded_string + "\n")
    
    substrings = decoded_string.split(" ")
    sum = 0
    for substr in substrings:
        temp_list = n_gram_substring(n_value, substr)
        for i in temp_list:
            if i in n_grams_dict:
                sum += math.log(int(n_grams_dict[i]), 2)
    cipher_fitness_dict[cipher] = sum
    
    return sum

def hill_climbing(encoded_string):
    word = list(real_alphabet)
    random.shuffle(word)
    cipher = ''.join(word)
    print(decode(encoded_string, make_decoder_alphabet(cipher)))
    best_result = (cipher, fitness(3, encoded_string, cipher))
    initial_cipher = cipher
    new_cipher = ""

    while True:
        index1 = random.randint(0, 25)
        index2 = random.randint(0, 25)
        while index1 == index2:
            index2 = random.randint(0, 25)
        
        if index2 > index1:     
            new_cipher = ''.join((initial_cipher[:index1], initial_cipher[index2], initial_cipher[index1+1:index2], initial_cipher[index1], initial_cipher[index2+1:]))
        else:
            new_cipher = ''.join((initial_cipher[:index2], initial_cipher[index1], initial_cipher[index2+1:index1], initial_cipher[index2], initial_cipher[index1+1:]))
        
        result_fitness = fitness(3, encoded_string, new_cipher)
        if result_fitness > best_result[1]:
            initial_cipher = new_cipher
            best_result = (new_cipher, result_fitness)
            print(decode(encoded_string, make_decoder_alphabet(new_cipher))) 
            print()       

def make_population(population_size):
    generation_set = set()
    while len(generation_set) < population_size:
        word = list(real_alphabet)
        random.shuffle(word)
        cipher = ''.join(word)
        generation_set.add(cipher)
    return generation_set

def choose_parent(parent_list, tournament_win_probability):
    for parent in parent_list:
        if random.random() < tournament_win_probability:
            return parent

def breed(parent1, parent2, crossover_locations):
    child = ""
    crossover_indices = []
    crossover_values = []

    #print(parent1[1], parent2[1])

    for j in range(crossover_locations):
        index = random.randint(0, 25)
        while index in crossover_indices:
            index = random.randint(0, 25)
        crossover_indices.append(index)
        crossover_values.append(parent1[1][index])

    count = 0
    for i in range(26):
        if i in crossover_indices:
            child += parent1[1][i]
        else:
            while (parent2[1][count] in child or parent2[1][count] in crossover_values) and count < 26:
                count += 1
            child += parent2[1][count]
            count += 1

    return child 

def selection(generation_set, population_size, encoded_string, num_clones, tournament_size, tournament_win_probability, crossover_locations, mutation_rate, generation_num):
    if generation_num >= 500:
        return 
    
    new_generation_set = set()

    #ranking generation
    rank_list = []
    for cipher in generation_set:
        cipher_fitness = fitness(3, encoded_string, cipher)
        rank_list.append((cipher_fitness, cipher))
    rank_list = sorted(rank_list, reverse=True)

    for i in range(num_clones):
        new_generation_set.add(rank_list[i][1])

    #print("ranking generation " + str(generation_num) + " done")

    #tournament
    tournament_set = set()
    while len(tournament_set) < (tournament_size * 2):
        random_index = random.randint(0, len(rank_list) - 1)
        tournament_set.add(rank_list[random_index][1])

    #print("tournament done")

    #parents
    parent1_list = []
    for j in range(tournament_size):
        cipher = tournament_set.pop()
        parent1_list.append((fitness(3, encoded_string, cipher), cipher))
    parent1_list = sorted(parent1_list, reverse=True)
    
    parent2_list = []
    for k in range(tournament_size):
        cipher = tournament_set.pop()
        parent2_list.append((fitness(3, encoded_string, cipher), cipher))
    parent2_list = sorted(parent2_list, reverse=True)

    #print("parents done")

    #breeding and mutations
    while len(new_generation_set) < population_size:
        parent1 = choose_parent(parent1_list, tournament_win_probability)
        parent2 = choose_parent(parent2_list, tournament_win_probability)

        child = breed(parent1, parent2, crossover_locations) + " "

        if random.random() < mutation_rate:
            index1 = random.randint(0, 25)
            index2 = random.randint(0, 25)
            while index1 == index2:
                index2 = random.randint(0, 25)
            
            if index2 > index1:
                #print(child, index1, index2)     
                child = ''.join((child[:index1], child[index2], child[index1+1:index2], child[index1], child[index2+1:]))
            else:
                #print(child, index2, index1)
                child = ''.join((child[:index2], child[index1], child[index2+1:index1], child[index2], child[index1+1:]))

        new_generation_set.add(child[:26])
    
    c = rank_list[0][1]
    cipher_alphabet = make_decoder_alphabet(c)
    decoded_string = decode(encoded_string, cipher_alphabet)

    # with open('readme.txt', 'w') as f:
    #     f.write(str(c) + "(" + str(fitness(3, encoded_string, c)) + "):\n" + decoded_string + "\n")
    # print()

    print("Generation " + str(generation_num) +": " + decoded_string)
    print()

    return selection(new_generation_set, population_size, encoded_string, num_clones, tournament_size, tournament_win_probability, crossover_locations, mutation_rate, generation_num + 1)

encoded_string = sys.argv[1]
selection(make_population(POPULATION_SIZE), POPULATION_SIZE, encoded_string, NUM_CLONES, TOURNAMENT_SIZE, TOURNAMENT_WIN_PROBABILITY, CROSSOVER_LOCATIONS, MUTATION_RATE, 0)

#word = list(real_alphabet)
#random.shuffle(word)
#cipher_actual = ''.join(word)

#cipher = "BACDEFGHIJKLMNOPQRSTUVWXYZ"
#cipher_actual_encoder = make_encoder_alphabet(cipher_actual)

#print((e := encode("banana! hey", cipher_actual_encoder)))
#print(decode(e, make_decoder_alphabet(cipher_actual)))

#print(fitness(3, "idk", "lol"))
#hill_climbing("PF HACYHTTRQ VF N PBYYRPGVBA BS SERR YRNEAVAT NPGVIVGVRF GUNG GRNPU PBZCHGRE FPVRAPR GUEBHTU RATNTVAT TNZRF NAQ CHMMYRF GUNG HFR PNEQF, FGEVAT, PENLBAF NAQ YBGF BS EHAAVAT NEBHAQ. JR BEVTVANYYL QRIRYBCRQ GUVF FB GUNG LBHAT FGHQRAGF PBHYQ QVIR URNQ-SVEFG VAGB PBZCHGRE FPVRAPR, RKCREVRAPVAT GUR XVAQF BS DHRFGVBAF NAQ PUNYYRATRF GUNG PBZCHGRE FPVRAGVFGF RKCREVRAPR, OHG JVGUBHG UNIVAT GB YRNEA CEBTENZZVAT SVEFG. GUR PBYYRPGVBA JNF BEVTVANYYL VAGRAQRQ NF N ERFBHEPR SBE BHGERNPU NAQ RKGRAFVBA, OHG JVGU GUR NQBCGVBA BS PBZCHGVAT NAQ PBZCHGNGVBANY GUVAXVAT VAGB ZNAL PYNFFEBBZF NEBHAQ GUR JBEYQ, VG VF ABJ JVQRYL HFRQ SBE GRNPUVAT. GUR ZNGREVNY UNF ORRA HFRQ VA ZNAL PBAGRKGF BHGFVQR GUR PYNFFEBBZ NF JRYY, VAPYHQVAT FPVRAPR FUBJF, GNYXF SBE FRAVBE PVGVMRAF, NAQ FCRPVNY RIRAGF. GUNAXF GB TRAREBHF FCBAFBEFUVCF JR UNIR ORRA NOYR GB PERNGR NFFBPVNGRQ ERFBHEPRF FHPU NF GUR IVQRBF, JUVPU NER VAGRAQRQ GB URYC GRNPUREF FRR UBJ GUR NPGVIVGVRF JBEX (CYRNFR QBA’G FUBJ GURZ GB LBHE PYNFFRF – YRG GURZ RKCREVRAPR GUR NPGVIVGVRF GURZFRYIRF!). NYY BS GUR NPGVIVGVRF GUNG JR CEBIVQR NER BCRA FBHEPR – GURL NER ERYRNFRQ HAQRE N PERNGVIR PBZZBAF NGGEVOHGVBA FUNERNYVXR YVPRAPR, FB LBH PNA PBCL, FUNER NAQ ZBQVSL GUR ZNGREVNY. SBE NA RKCYNANGVBA BA GUR PBAARPGVBAF ORGJRRA PF HACYHTTRQ NAQ PBZCHGNGVBANY GUVAXVAT FXVYYF, FRR BHE PBZCHGNGVBANY GUVAXVAT NAQ PF HACYHTTRQ CNTR. GB IVRJ GUR GRNZ BS PBAGEVOHGBEF JUB JBEX BA GUVF CEBWRPG, FRR BHE CRBCYR CNTR. SBE QRGNVYF BA UBJ GB PBAGNPG HF, FRR BHE PBAGNPG HF CNTR. SBE ZBER VASBEZNGVBA NOBHG GUR CEVAPVCYRF ORUVAQ PF HACYHTTRQ, FRR BHE CEVAPVCYRF CNTR.")