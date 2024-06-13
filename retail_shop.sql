--
-- Database: `retail_shop`
--

-- --------------------------------------------------------

--
-- Table structure for table `branch`
--

CREATE TABLE `branch` (
  `BranchID` int(11) NOT NULL,
  `BranchAddress` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `branch`
--

INSERT INTO `branch` (`BranchID`, `BranchAddress`) VALUES
(1, 'June St.'),
(2, 'May St.');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `CustomerID` int(11) NOT NULL,
  `CustName` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Phone` varchar(255) DEFAULT NULL,
  `CustAddress` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`CustomerID`, `CustName`, `Email`, `Phone`, `CustAddress`) VALUES
(33259, 'Frank Moore', 'frank@example.com', '5553334444', '987 Elm St'),
(43606, 'Alice Johnson', 'alice@example.com', '1234567890', '123 Maple St'),
(49196, 'Charlie Brown', 'charlie@example.com', '5551234567', '789 Pine St'),
(62541, 'Bob Smith', 'bob@example.com', '9876543210', '456 Oak st'),
(73972, 'David Wilson', 'david@example.com', '5551112222', '654 Cedar St'),
(98085, 'Sam', 'sam@gmail', '121412312', 'abcde');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `BranchID` int(11) NOT NULL,
  `EmployeeID` int(11) NOT NULL,
  `EmpName` varchar(255) DEFAULT NULL,
  `Position` varchar(255) DEFAULT NULL,
  `Salary` decimal(10,2) DEFAULT NULL,
  `HireDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`BranchID`, `EmployeeID`, `EmpName`, `Position`, `Salary`, `HireDate`) VALUES
(2, 1, 'Bob Brown', 'Cashier', 35000.00, '2018-05-01'),
(2, 2, 'Samantha Green', 'Manager', 50000.00, '2017-08-15'),
(2, 3, 'Daniel Blue', 'Stock Clerk', 25000.00, '2019-06-10'),
(1, 4, 'John Smith', 'Manager', 50000.00, '2020-01-15'),
(1, 5, 'Jane Doe', 'Sales Associate', 40000.00, '2021-06-01');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `ProductID` int(11) NOT NULL,
  `ProdName` varchar(255) DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `StockQuantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`ProductID`, `ProdName`, `Price`, `Description`, `StockQuantity`) VALUES
(1, 'Blue T-shirt', 24.99, 'Cotton blue t-shirt in size M', 22),
(2, 'Leather Wallet', 29.99, 'Genuine leather wallet', 26),
(3, 'Running Shoes', 59.99, 'High-quality running shoes', 40),
(4, 'Laptop', 699.99, 'High performance laptop', 26),
(5, 'Smart Phone', 599.99, 'Latest model smart phone', 22);

-- --------------------------------------------------------

--
-- Table structure for table `sale`
--

CREATE TABLE `sale` (
  `SaleID` int(11) NOT NULL,
  `BranchID` int(11) NOT NULL,
  `Date` date DEFAULT NULL,
  `TotalAmount` decimal(10,2) DEFAULT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `EmployeeID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sale`
--

INSERT INTO `sale` (`SaleID`, `BranchID`, `Date`, `TotalAmount`, `CustomerID`, `EmployeeID`) VALUES
(14806, 2, '2023-06-23', 2799.96, 98085, 3),
(20569, 1, '2024-06-07', 2249.92, 49196, 2),
(28551, 1, '2023-06-08', 12599.82, 98085, 3),
(32600, 2, '2023-06-08', 74.97, 98085, 2),
(45017, 2, '2024-06-07', 1034.89, 73972, 2),
(52943, 1, '2023-06-08', 1764.64, 98085, 3),
(55890, 2, '2024-06-13', 6199.82, 98085, 1),
(58292, 1, '2024-06-08', 3029.94, 33259, 1),
(70222, 2, '2024-06-06', 74.97, 43606, 1),
(71115, 1, '2023-06-08', 49.98, 98085, 2),
(72555, 1, '2023-06-16', 13799.77, 98085, 2),
(93474, 2, '2024-06-07', 239.92, 33259, 1);

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
(14806, 4, 4),
(20569, 2, 5),
(20569, 4, 3),
(28551, 4, 9),
(32600, 1, 3),
(45017, 1, 5),
(52943, 1, 1),
(55890, 4, 8),
(58292, 2, 1),
(58292, 5, 5),
(70222, 1, 3),
(71115, 1, 2),
(72555, 5, 23),
(93474, 2, 8);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `branch`
--
ALTER TABLE `branch`
  ADD PRIMARY KEY (`BranchID`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`CustomerID`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`EmployeeID`),
  ADD KEY `BranchID` (`BranchID`);

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
  ADD KEY `EmployeeID` (`EmployeeID`),
  ADD KEY `BranchID` (`BranchID`);

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
-- Constraints for table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`BranchID`) REFERENCES `branch` (`BranchID`);

--
-- Constraints for table `sale`
--
ALTER TABLE `sale`
  ADD CONSTRAINT `sale_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  ADD CONSTRAINT `sale_ibfk_2` FOREIGN KEY (`EmployeeID`) REFERENCES `employee` (`EmployeeID`),
  ADD CONSTRAINT `sale_ibfk_3` FOREIGN KEY (`BranchID`) REFERENCES `branch` (`BranchID`);

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
