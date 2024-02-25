using GenX 

config = GenX.Configuration("*.toml")

model = GenX.build_model(config)

GenX.solve!(model)

results = GenX.get_results(model)

