-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema vendas
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema vendas
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `vendas` DEFAULT CHARACTER SET utf8mb3 ;
USE `vendas` ;

-- -----------------------------------------------------
-- Table `vendas`.`clientes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vendas`.`clientes` ;

CREATE TABLE IF NOT EXISTS `vendas`.`clientes` (
  `ID_cliente` INT NOT NULL AUTO_INCREMENT,
  `nome_cliente` VARCHAR(100) NOT NULL,
  `cpf_cliente` VARCHAR(11) NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `data_cadastro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_cliente`),
  UNIQUE INDEX `cpf_cliente_UNIQUE` (`cpf_cliente` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 501
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `vendas`.`contato`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vendas`.`contato` ;

CREATE TABLE IF NOT EXISTS `vendas`.`contato` (
  `ID_contato` INT NOT NULL AUTO_INCREMENT,
  `tipo_contato` ENUM('E-mail', 'Telefone', 'WhatsApp') NOT NULL,
  `valor_contato` VARCHAR(100) NOT NULL,
  `clientes_ID_cliente` INT NOT NULL,
  PRIMARY KEY (`ID_contato`),
  INDEX `fk_contato_clientes_idx` (`clientes_ID_cliente` ASC) VISIBLE,
  CONSTRAINT `fk_contato_clientes_final`
    FOREIGN KEY (`clientes_ID_cliente`)
    REFERENCES `vendas`.`clientes` (`ID_cliente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `vendas`.`endereco`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vendas`.`endereco` ;

CREATE TABLE IF NOT EXISTS `vendas`.`endereco` (
  `ID_endereco` INT NOT NULL AUTO_INCREMENT,
  `logradouro` VARCHAR(100) NOT NULL,
  `numero` VARCHAR(20) NOT NULL,
  `complemento` VARCHAR(45) NULL DEFAULT NULL,
  `bairro` VARCHAR(45) NOT NULL,
  `cidade` VARCHAR(45) NOT NULL,
  `estado` VARCHAR(2) NOT NULL,
  `cep` VARCHAR(8) NOT NULL,
  `tipo_endereco` ENUM('Residencial', 'Entrega', 'Cobrança') NOT NULL,
  `clientes_ID_cliente` INT NOT NULL,
  PRIMARY KEY (`ID_endereco`),
  INDEX `fk_endereco_clientes_idx` (`clientes_ID_cliente` ASC) VISIBLE,
  CONSTRAINT `fk_endereco_clientes_final`
    FOREIGN KEY (`clientes_ID_cliente`)
    REFERENCES `vendas`.`clientes` (`ID_cliente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `vendas`.`pedidos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vendas`.`pedidos` ;

CREATE TABLE IF NOT EXISTS `vendas`.`pedidos` (
  `ID_pedidos` INT NOT NULL AUTO_INCREMENT,
  `data_pedido` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status_pedido` ENUM('Pendente', 'Pago', 'Processando', 'Enviado', 'Entregue', 'Cancelado') NOT NULL,
  `valor_total` DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT '0.00',
  `clientes_ID_cliente` INT NOT NULL,
  PRIMARY KEY (`ID_pedidos`),
  INDEX `fk_pedidos_clientes_idx` (`clientes_ID_cliente` ASC) VISIBLE,
  CONSTRAINT `fk_pedidos_clientes_final`
    FOREIGN KEY (`clientes_ID_cliente`)
    REFERENCES `vendas`.`clientes` (`ID_cliente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `vendas`.`produtos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vendas`.`produtos` ;

CREATE TABLE IF NOT EXISTS `vendas`.`produtos` (
  `ID_produto` INT NOT NULL AUTO_INCREMENT,
  `nome_produto` VARCHAR(100) NOT NULL,
  `descricao_produto` TEXT NOT NULL,
  `preco_produto` DECIMAL(10,2) UNSIGNED NOT NULL,
  `estoque_produto` INT UNSIGNED NOT NULL,
  `categoria_produto` ENUM('Eletrônicos', 'Roupas', 'Alimentos', 'Outros') NOT NULL,
  PRIMARY KEY (`ID_produto`))
ENGINE = InnoDB
AUTO_INCREMENT = 101
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `vendas`.`pedido_itens`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vendas`.`pedido_itens` ;

CREATE TABLE IF NOT EXISTS `vendas`.`pedido_itens` (
  `quantidade` INT UNSIGNED NOT NULL,
  `preco_unitario_historico` DECIMAL(10,2) UNSIGNED NOT NULL,
  `produtos_ID_produto` INT NOT NULL,
  `pedidos_ID_pedidos` INT NOT NULL,
  PRIMARY KEY (`produtos_ID_produto`, `pedidos_ID_pedidos`),
  INDEX `fk_pedido_itens_produtos_idx` (`produtos_ID_produto` ASC) VISIBLE,
  INDEX `fk_pedido_itens_pedidos_idx` (`pedidos_ID_pedidos` ASC) VISIBLE,
  CONSTRAINT `fk_itens_pedidos_final`
    FOREIGN KEY (`pedidos_ID_pedidos`)
    REFERENCES `vendas`.`pedidos` (`ID_pedidos`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_itens_produtos_final`
    FOREIGN KEY (`produtos_ID_produto`)
    REFERENCES `vendas`.`produtos` (`ID_produto`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
