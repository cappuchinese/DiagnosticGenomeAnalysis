DROP TABLE IF EXISTS Chromosome;
DROP TABLE IF EXISTS Genes;
DROP TABLE IF EXISTS Variants;

CREATE TABLE Chromosome(
    id          INT             AUTO_INCREMENT,
    chr         VARCHAR(5)      NOT NULL,
    primary key(id)
);

CREATE TABLE Genes(
    id          INT             AUTO_INCREMENT,
    gene        VARCHAR(20)     NOT NULL,
    primary key(id)
);

CREATE TABLE Variants(
    id                      INT             AUTO_INCREMENT,
    chromosome              VARCHAR(5)      NOT NULL,
    gene                    VARCHAR(20)     NOT NULL,
    ref                     CHAR(1)         NOT NULL,
    func                    VARCHAR(15)     NOT NULL,
    dbsnp138                VARCHAR(15)     ,
    1000g2015_EUR           FLOAT           ,
    LJB2_SIFT               FLOAT           ,
    LJB2_PolyPhen2_HDIV     VARCHAR(10)     ,
    LJB2_PolyPhen2_HVAR     VARCHAR(10)     ,
    CLINVAR                 VARCHAR(130)    ,
    constraint chromosome foreign key (chromosome)
        references Chromosome(chr),
    constraint gene foreign key (gene)
        references Genes(gene)
);
