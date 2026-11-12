-- Patient table
CREATE TABLE IF NOT EXISTS Patient  (
    pid TEXT PRIMARY KEY NOT NULL,
    CancerStatus TEXT NOT NULL
);

-- Gene Table
CREATE TABLE IF NOT EXISTS Gene  (
    GeneName TEXT PRIMARY KEY,
    Chromosome INT NOT NULL
);

-- Mutation table
CREATE TABLE IF NOT EXISTS Mutation  (
    MID TEXT PRIMARY KEY NOT NULL,
    GeneName TEXT NOT NULL REFERENCES Gene(Genename),
    MutationType TEXT NOT NULL,
    PolyType TEXT NOT NULL,
    StartCoord INT NOT NULL,
    EndCoord INT NOT NULL,
    StartNucleotide TEXT NOT NULL
);

-- Has_Mutation Table
CREATE TABLE IF NOT EXISTS HasMutation (
    PID TEXT NOT NULL,
    MID TEXT NOT NULL,
    PRIMARY KEY (PID, MID),
    FOREIGN KEY (PID) REFERENCES Patient(PID),
    FOREIGN KEY (MID) REFERENCES Mutation(MID)
);

--End_Nucleotide Table
CREATE TABLE IF NOT EXISTS End_Nucleotide (
    MID TEXT NOT NULL,
    Nucleotide TEXT NOT NULL,
    PRIMARY KEY (MID, Nucleotide),
    FOREIGN KEY (MID) REFERENCES Mutation(MID)
);



