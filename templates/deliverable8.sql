DROP TABLE IF EXISTS Chromosome;
DROP TABLE IF EXISTS Genes;
DROP TABLE IF EXISTS Variants;

CREATE TABLE Chromosome(
    chr_id      INT             AUTO_INCREMENT,
    chromosome  VARCHAR(5)      NOT NULL UNIQUE,
    primary key(chr_id)
);

CREATE TABLE Genes(
    gene_id         INT             AUTO_INCREMENT,
    RefSeq_Gene     VARCHAR(20)     NOT NULL,
    chromosome      INT             REFERENCES Chromosome(chr_id),
    primary key(gene_id)
);

CREATE TABLE Variants(
    id                      INT             AUTO_INCREMENT UNIQUE,
    chromosome              VARCHAR(5)      REFERENCES Chromosome(chr_id),
    RefSeq_Gene             VARCHAR(20)     REFERENCES Genes(gene_id),
    reference               CHAR(1)         NOT NULL,
    RefSeq_Func             VARCHAR(15)     NOT NULL,
    dbsnp138                VARCHAR(15)     ,
    1000g2015_EUR           VARCHAR(15)     ,
    LJB2_SIFT               VARCHAR(15)     ,
    LJB2_PolyPhen2_HDIV     VARCHAR(10)     ,
    LJB2_PolyPhen2_HVAR     VARCHAR(10)     ,
    CLINVAR                 VARCHAR(130)    ,
    primary key(id)
);
