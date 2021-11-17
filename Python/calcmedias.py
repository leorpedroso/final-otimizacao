
sol_inicial = []
sol_final = []

files = ['01', '02', '03', '04', '05', '06', '07', '08', '09', 
          '10', '11', '12']

seeds = ['10', '69', '100', '1337', '80085']

referencia = [2436, 2432, 2436, 2439, 2436, 2431,
              2437, 2433, 2436, 2429, 2434, 2440]

julia_final = [2182, 2173, 2159, 2171, 2132, 2153,
               2169, 2173, 2188, 2144, 2164, 2161]

bounds = [1, 1250, 2500]
steps = [1, 10, 100]
# RM
# for n in range(len(files)):
#   sol_inicial = []
#   sol_final = []
#   for i in seeds:
#     filename = f'results/instances/rm{files[n]}_{i}'
#     try:
#       with open(filename) as f:
#         sol_inicial.append(int(f.readline()))
#         sol_final.append(int(f.readline()))
#     except FileNotFoundError as e:
#       continue

#   media_inicial = sum(sol_inicial)/len(sol_inicial)
#   media_final = sum(sol_final)/len(sol_final)
#   desvio_inicio = 100*(media_inicial-media_final)/media_inicial
#   desvio_ref = 100*(referencia[n]-media_final)/referencia[n]
#   desvio_ref_julia = 100*(referencia[n]-julia_final[n])/referencia[n]
#   # print('='*15)
#   # print(f'RM{files[n]}')
#   # print(media_inicial)
#   # print(media_final)
#   # print(desvio_inicio)
#   # print(desvio_ref)
#   # print(desvio_ref_julia)
  
#   # print(desvio_ref_julia)

# Range

# for n in range(2):
#   sol_final = []
#   for i in seeds:
#     filename = f'results/random/random_{bounds[n]}_{i}'
#     try:
#       with open(filename) as f:
#         sol_final.append(int(f.readline()))
#     except FileNotFoundError as e:
#       print(e)

#   print(sum(sol_final)/len(sol_final))

# for i in seeds:
#   sol_final = []
#   filename = f'results/random/random_{bounds[2]}_{i}'
#   try:
#     with open(filename) as f:
#       sol_inicial.append(int(f.readline()))
#       sol_final.append(int(f.readline()))
#   except FileNotFoundError as e:
#     print(e)

# print(sum(sol_final)/len(sol_final))

# Step
for n in range(2):
  for i in seeds:
    sol_final = []
    filename = f'results/step/step_{steps[n]}_{i}'
    try:
      with open(filename) as f:
        sol_inicial.append(int(f.readline()))
        sol_final.append(int(f.readline()))
    except FileNotFoundError as e:
      print(e)

  print(sum(sol_final)/len(sol_final))

