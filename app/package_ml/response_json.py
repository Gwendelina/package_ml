class Response_json:
    def __init__(self):
        self.f_v = 0
        self.f_m = 0
        self.h_v = 0
        self.h_m = 0
        self.pclass1_v = 0
        self.pclass1_m = 0
        self.pclass2_v = 0
        self.pclass2_m = 0
        self.pclass3_v = 0
        self.pclass3_m = 0

    
    # features[1] = 1 (femme) / = 0 (homme) 
    # target[0] = 1 (survived) / = 0 (dead)
    def sex_survived(self, X, y):
        for features, target in zip(X.values, y.values):
            if int(features[1]) == 1 and target[0] == 1:
                self.f_v += 1
            elif int(features[1]) == 1 and target[0] == 0:
                self.f_m += 1
            elif int(features[1]) == 0 and target[0] == 1:
                self.h_v += 1
            elif int(features[1]) == 0 and target[0] == 0:
                self.h_m += 1
        return [{"name":"Nombre de femmes ayant survécu","pourcent":self.f_v},{"name":"Nombre de femmes n'ayant pas survécu", "pourcent":self.f_m},
                {"name":"Nombre d'hommes ayant survécu", "pourcent":self.h_v},{"name":"Nombre d'hommes n'ayant pas survécu", "pourcent":self.h_m}]       


    def pclass_survived(self, X, y):
        for features, target in zip(X.values, y.values):
            if int(features[0]) == 1 and target[0] == 1:
                self.pclass1_v += 1
            elif int(features[0]) == 1 and target[0] == 0:
                self.pclass1_m += 1
            elif int(features[0]) == 2 and target[0] == 1:
                self.pclass2_v += 1
            elif int(features[0]) == 2 and target[0] == 0:
                self.pclass2_m += 1
            elif int(features[0]) == 3 and target[0] == 1:
                self.pclass3_v += 1
            elif int(features[0]) == 3 and target[0] == 0:
                self.pclass3_m += 1
        return [{"name": "Nombre de survivants ayant un ticket en 1ère classe","pourcent": self.pclass1_v},
        {"name":"Nombre de morts ayant un ticket en 1ère classe","pourcent":self.pclass1_m},
        {"name":"Nombre de survivants ayant un ticket en 2ème classe","pourcent":self.pclass2_v},
        {"name":"Nombre de morts ayant un ticket en 2ème classe","pourcent":self.pclass2_m},
        {"name":"Nombre de survivants ayant un ticket en 3ème classe","pourcent":self.pclass3_v},
        {"name":"Nombre de morts ayant un ticket en 3ème classe","pourcent":self.pclass3_m}]

