-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS loja;
USE loja;

-- Tabela de Categorias
CREATE TABLE `categorias` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Inserir dados de exemplo na tabela de Categorias
INSERT INTO `categorias` (`nome`) VALUES
('Bebida'),
('Alimento'),
('Limpeza');

-- Tabela de Clientes
CREATE TABLE `clientes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `telefone` VARCHAR(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Inserir dados de exemplo na tabela de Clientes
INSERT INTO `clientes` (`nome`, `email`, `telefone`) VALUES
('Marcus', 'marcus@teste.com', '41837928429'),
('Ana', 'ana@teste.com', '41837928430');

-- Tabela de Produtos
CREATE TABLE `produtos` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `preco` FLOAT NOT NULL,
  `estoque` INT(11) NOT NULL,
  `categoriaid` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`categoriaid`) REFERENCES `categorias` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Inserir dados de exemplo na tabela de Produtos
INSERT INTO `produtos` (`nome`, `preco`, `estoque`, `categoriaid`) VALUES
('Refrigerante', 5.50, 100, 1),
('Pão', 1.50, 200, 2),
('Detergente', 3.00, 150, 3);

-- Tabela de Vendas
CREATE TABLE `vendas` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `produtoid` INT(11) NOT NULL,
  `clienteid` INT(11) NOT NULL,
  `quantidade` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`produtoid`) REFERENCES `produtos` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`clienteid`) REFERENCES `clientes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Inserir dados de exemplo na tabela de Vendas
INSERT INTO `vendas` (`produtoid`, `clienteid`, `quantidade`) VALUES
(1, 1, 2),
(2, 2, 1);
