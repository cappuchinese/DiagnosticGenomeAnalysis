SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS Chromosomes;
DROP TABLE IF EXISTS Genes;
DROP TABLE IF EXISTS Variants;

CREATE TABLE Chromosomes(
    chr_id      INT             AUTO_INCREMENT,
    chromosome  VARCHAR(20)      NOT NULL UNIQUE,
    primary key(chr_id)
);
CREATE TABLE Genes(
    gene_id         INT             AUTO_INCREMENT,
    RefSeq_Gene     VARCHAR(150)     NOT NULL,
    chr_id          INT             REFERENCES Chromosomes(chr_id),
    primary key(gene_id)
);
CREATE TABLE Variants(
    id                      INT             AUTO_INCREMENT UNIQUE,
    chr_id                  INT             REFERENCES Chromosomes(chr_id),
    gene_id                 INT             REFERENCES Genes(gene_id),
    reference               CHAR(1)         NOT NULL,
    observed                CHAR(1)         ,
    RefSeq_Func             VARCHAR(48)     NOT NULL,
    dbsnp138                VARCHAR(15)     ,
    1000g2015_EUR           VARCHAR(15)     ,
    LJB2_SIFT               VARCHAR(15)     ,
    LJB2_PolyPhen2_HDIV     VARCHAR(10)     ,
    LJB2_PolyPhen2_HVAR     VARCHAR(10)     ,
    CLINVAR                 VARCHAR(130)    ,
    primary key(id),
    CONSTRAINT FOREIGN KEY (chr_id) REFERENCES Chromosomes(chr_id) ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (gene_id) REFERENCES Genes(gene_id) ON DELETE CASCADE
);
