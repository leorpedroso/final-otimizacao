using JuMP
using GLPK

m = Model();
set_optimizer(m, GLPK.Optimizer);

# tempo limite de 30 minutos
set_time_limit_sec(m, 1800.0);

function reader(filepath :: String)
  k_count = 0
  arestas = []
  v_count = 0
  
  open(filepath, "r") do f
    line = readline(f)
    line = readline(f)
    v_count = parse(Int, line) # Number of vertices
    line = readline(f)
    line = readline(f)

    while ! eof(f)
      line = readline(f)
      words = split(line)
      if isempty(words)
          continue
      end
      vertex1 = parse(Int,words[1])
      vertex2 = parse(Int,words[2])
      edge_type = parse(Int,words[3])

      # o numero de tipos de arestas eh igual ao maior tipo
      if edge_type > k_count
        k_count = edge_type
      end

      push!(arestas, (vertex1,vertex2,edge_type))
    end
  end
  return (arestas, k_count, v_count)
end

print("Digite o arquivo da instância: ")
filepath = readline()

my_tuple = reader(filepath)
arestas = my_tuple[1]
K = my_tuple[2]
V = my_tuple[3];

function create_arestas_k(arestas, k)
  # Retorna uma lista de listas que contem arestas do tipo k
  # Por exemplo, se a aresta tem tipo 10, sera inserida na 
  # lista na posicao correspondente 
    arestas_k = [[] for i=1:k]
    for a in arestas
        push!(arestas_k[a[3]], (a))
    end
    return arestas_k
end

arestas_k = create_arestas_k(arestas,K);

# Variavel x tem valor 1 se a aresta eh escolhida, 0 caso contrario
@variable(m, x[i in arestas], Bin);

# No maximo uma aresta de cada tipo pode estar na solucao
@constraint(m, [k in 1:K], sum(x[i] for i in arestas_k[k]) <=1);

function create_arestas_v(arestas, v)
  # Retorna uma lista de listas que contem arestas que incidem
  # sobre o vertice na respectiva posicao
  # Por exemplo, a aresta 4-5 sera inserida nas 
  # listas que estao nas posicoes 4 e 5
    arestas_v = [[] for i=1:v]
    for a in arestas
        push!(arestas_v[a[1]], (a))
        push!(arestas_v[a[2]], (a))
    end
    return arestas_v
end

arestas_v = create_arestas_v(arestas,V);

# No maximo uma aresta pode incidir sobre cada vertice
@constraint(m, [v in 1:V], sum(x[i] for i in arestas_v[v]) <=1);

@objective(m, Max, sum(x[i] for i in arestas));

optimize!(m)

objective_value(m)

print(value.(x))


open(ARGS[1], "w") do f
  write(f, string.(objective_value(m)) * "\n")
  for i in (x)
      write(f, string.(i) * " " * string.(value.(i)) * "\n")
  end
end
