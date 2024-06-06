--
-- Database: `retail_shop`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `CustomerID` int(11) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Phone` varchar(255) DEFAULT NULL,
  `Address` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`CustomerID`, `Name`, `Email`, `Phone`, `Address`) VALUES
(1, 'John Doe', 'john.doe@example.com', '1234567890', '123 Maple Street'),
(2, 'Jane Smith', 'jane.smith@example.com', '0987654321', '456 Oak Avenue'),
(3, 'Alice Johnson', 'alice.johnson@example.com', '1029384756', '789 Pine Road'),

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `EmployeeID` int(11) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Position` varchar(255) DEFAULT NULL,
  `Salary` decimal(10,2) DEFAULT NULL,
  `HireDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`EmployeeID`, `Name`, `Position`, `Salary`, `HireDate`) VALUES
(1, 'Bob Brown', 'Cashier', 30000.00, '2018-05-01'),
(2, 'Samantha Green', 'Manager', 50000.00, '2017-08-15'),
(3, 'Daniel Blue', 'Stock Clerk', 25000.00, '2019-06-10'),

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `ProductID` int(11) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `StockQuantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`ProductID`, `Name`, `Price`, `Description`, `StockQuantity`) VALUES
(1, 'Blue T-shirt', 19.99, 'Cotton blue t-shirt in size M', 34),
(2, 'Leather Wallet', 29.99, 'Genuine leather wallet', 29),
(3, 'Running Shoes', 59.99, 'High-quality running shoes', 20);

-- --------------------------------------------------------

--
-- Table structure for table `sale`
--

CREATE TABLE `sale` (
  `SaleID` int(11) NOT NULL,
  `Date` date DEFAULT NULL,
  `TotalAmount` decimal(10,2) DEFAULT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `EmployeeID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sale`
--

INSERT INTO `sale` (`SaleID`, `Date`, `TotalAmount`, `CustomerID`, `EmployeeID`) VALUES
(1, '2024-06-01', 89.97, 1, 1),
(2, '2024-06-02', 29.99, 2, 1),
(3, '2024-06-03', 59.99, 3, 2),

-- --------------------------------------------------------

--
-- Table structure for table `saleproduct`
--

CREATE TABLE `saleproduct` (
  `SaleID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `Quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `saleproduct`
--

INSERT INTO `saleproduct` (`SaleID`, `ProductID`, `Quantity`) VALUES
(1, 1, 2),
(1, 2, 1),
(2, 2, 1),
(3, 3, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`CustomerID`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`EmployeeID`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`ProductID`);

--
-- Indexes for table `sale`
--
ALTER TABLE `sale`
  ADD PRIMARY KEY (`SaleID`),
  ADD KEY `CustomerID` (`CustomerID`),
  ADD KEY `EmployeeID` (`EmployeeID`);

--
-- Indexes for table `saleproduct`
--
ALTER TABLE `saleproduct`
  ADD PRIMARY KEY (`SaleID`,`ProductID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sale`
--
ALTER TABLE `sale`
  ADD CONSTRAINT `sale_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  ADD CONSTRAINT `sale_ibfk_2` FOREIGN KEY (`EmployeeID`) REFERENCES `employee` (`EmployeeID`);

--
-- Constraints for table `saleproduct`
--
ALTER TABLE `saleproduct`
  ADD CONSTRAINT `saleproduct_ibfk_1` FOREIGN KEY (`SaleID`) REFERENCES `sale` (`SaleID`),
  ADD CONSTRAINT `saleproduct_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
