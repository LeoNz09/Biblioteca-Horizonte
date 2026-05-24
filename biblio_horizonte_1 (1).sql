-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-05-2026 a las 09:34:25
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `biblio_horizonte_1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administradores`
--

CREATE TABLE `administradores` (
  `id_admin` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administradores`
--

INSERT INTO `administradores` (`id_admin`, `nombre`, `correo`, `contraseña`) VALUES
(1, 'Leo', 'leo@biblio.com', 'admin123'),
(2, 'Lizeth', 'lizz@biblio.com', 'admin456');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devolucion`
--

CREATE TABLE `devolucion` (
  `id_devolucion` int(11) NOT NULL,
  `matricula` varchar(20) NOT NULL,
  `titulo_libro` varchar(255) NOT NULL,
  `nombre_prestamista` varchar(255) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `devolucion`
--

INSERT INTO `devolucion` (`id_devolucion`, `matricula`, `titulo_libro`, `nombre_prestamista`, `fecha`) VALUES
(58, '183375', 'Cien Años de Soledad', '183375', '2026-05-24 07:02:42'),
(59, '183375', 'Un Mundo Feliz', '183375', '2026-05-24 07:02:42'),
(60, '183375', 'Metamorfosis', '183375', '2026-05-24 07:02:42'),
(61, '183375', 'El Alquimista', '183375', '2026-05-24 07:02:42'),
(62, '183375', 'El Hobbit', '183375', '2026-05-24 07:02:42'),
(63, '183375', 'Frankenstein', '183375', '2026-05-24 07:03:07'),
(64, '183375', 'La Tregua', '183375', '2026-05-24 07:03:07'),
(65, '180010', 'Como Agua para Chocolate', '180010', '2026-05-24 07:04:56'),
(66, '180010', 'La Sombra del Viento', '180010', '2026-05-24 07:04:56'),
(67, '180010', 'El Retrato de Dorian Gray', '180010', '2026-05-24 07:04:56'),
(68, '180010', 'Paula', '180010', '2026-05-24 07:10:41'),
(69, '180010', 'La Casa de los Espiritus', '180010', '2026-05-24 07:12:41'),
(70, '180010', 'Como Agua para Chocolate', '180010', '2026-05-24 07:12:41'),
(71, '183375', 'Don Quijote de la Mancha', '183375', '2026-05-24 07:20:02'),
(72, '183375', 'El Principito', '183375', '2026-05-24 07:20:02'),
(73, '183375', 'La Casa de los Espiritus', '183375', '2026-05-24 07:20:02'),
(74, '183375', 'Paula', '183375', '2026-05-24 07:20:02'),
(75, '183375', 'Cien Años de Soledad', '183375', '2026-05-24 07:20:02'),
(76, '183375', 'Como Agua para Chocolate', '183375', '2026-05-24 07:20:02'),
(77, '183375', 'Frankenstein', '183375', '2026-05-24 07:20:02'),
(78, '183375', 'Cien Años de Soledad', '183375', '2026-05-24 07:31:45'),
(79, '183375', 'Don Quijote de la Mancha', '183375', '2026-05-24 07:31:45'),
(80, '183375', 'La Sombra del Viento', '183375', '2026-05-24 07:31:45'),
(81, '183375', 'La Fiesta del Chivo', '183375', '2026-05-24 07:31:45');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `id_estudiante` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `matricula` varchar(20) NOT NULL,
  `carrera` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`id_estudiante`, `nombre`, `apellidos`, `matricula`, `carrera`, `correo`) VALUES
(1, 'Leonardo', 'Núñez', '183782', 'ITI', '183782@biblio.com'),
(2, 'Maribel', 'Aguilar', '183375', 'ITI', '183375@biblio.com'),
(3, 'Juan', 'Hernández', '180010', 'ITMA', '180010@biblio.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial`
--

CREATE TABLE `historial` (
  `id_historial` int(11) NOT NULL,
  `titulo_libro` varchar(150) NOT NULL,
  `nombre_prestamista` varchar(100) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `id_libro` int(11) NOT NULL,
  `titulo` varchar(150) NOT NULL,
  `autor` varchar(100) NOT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `isbn` varchar(50) DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `disponibles` int(11) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`id_libro`, `titulo`, `autor`, `categoria`, `isbn`, `cantidad`, `disponibles`, `descripcion`) VALUES
(1, 'Cien Años de Soledad', 'Gabriel Garcia Marquez', 'Novela', '9780307474728', 5, 3, 'Historia de la familia Buendia en Macondo'),
(2, '1984', 'George Orwell', 'Distopia', '9780451524935', 3, 0, 'Sociedad controlada por el Gran Hermano'),
(3, 'El Principito', 'Antoine de Saint-Exupery', 'Infantil', '9780156012195', 4, 0, 'Fabula sobre la vida y la amistad'),
(4, 'Don Quijote de la Mancha', 'Miguel de Cervantes', 'Clasico', '9788491050295', 2, 1, 'Historia del caballero andante'),
(5, 'La Casa de los Espiritus', 'Isabel Allende', 'Novela', '9780553383805', 6, 5, 'Saga familiar ambientada en Chile con elementos de realismo magico'),
(6, 'Paula', 'Isabel Allende', 'Biografico', '9780060542183', 4, 3, 'Memoria escrita por Isabel Allende dedicada a su hija'),
(7, 'Como Agua para Chocolate', 'Laura Esquivel', 'Realismo Magico', '9780385420174', 5, 4, 'Historia de amor y tradicion mexicana mezclada con cocina'),
(8, 'La Sombra del Viento', 'Carlos Ruiz Zafon', 'Misterio', '9788408172178', 5, 4, 'Novela ambientada en Barcelona sobre libros y secretos'),
(9, 'El Amor en los Tiempos del Colera', 'Gabriel Garcia Marquez', 'Novela', '9780307389732', 3, 1, 'Historia de amor que perdura durante decadas'),
(10, 'La Fiesta del Chivo', 'Mario Vargas Llosa', 'Novela Historica', '9780374536996', 4, 4, 'Relato sobre la dictadura de Trujillo en Republica Dominicana'),
(11, 'La Casa de los Conejos', 'Laura Alcoba', 'Novela Historica', '9789876290199', 3, 3, 'Historia ambientada en la dictadura argentina'),
(12, 'Arrancame la Vida', 'Angeles Mastretta', 'Novela', '9789684110787', 4, 3, 'Historia de una mujer en el Mexico posrevolucionario'),
(13, 'Del Amor y Otros Demonios', 'Gabriel Garcia Marquez', 'Novela', '9780307473134', 3, 2, 'Historia inspirada en una leyenda colonial'),
(15, 'El Cuaderno de Maya', 'Isabel Allende', 'Novela', '9788401340468', 4, 2, 'Cuenta las peripecias de una joven perdida en el mundo del alcohol, las drogas y cómo poco a poco se abre paso hacia una nueva vida.'),
(16, 'Pedro Paramo', 'Juan Rulfo', 'Realismo Magico', '9789685208536', 5, 4, 'Un viaje a Comala, un pueblo de murmullos y fantasmas'),
(17, 'Ficciones', 'Jorge Luis Borges', 'Literatura', '9788420633138', 4, 3, 'Coleccion de cuentos que desafian la logica y el tiempo'),
(18, 'Rayuela', 'Julio Cortazar', 'Novela', '9788420471013', 3, 2, 'Novela contranovela que se puede leer en multiples ordenes'),
(19, 'Frankenstein', 'Mary Shelley', 'Terror', '9780143131847', 4, 2, 'Clasico de ciencia ficcion sobre el doctor y su criatura'),
(20, 'Dune', 'Frank Herbert', 'Ciencia Ficcion', '9780441172719', 6, 5, 'Epopeya planetaria sobre politica, religion y ecologia'),
(21, 'Dracula', 'Bram Stoker', 'Terror', '9780486411095', 5, 5, 'La legendaria historia del conde vampiro de Transilvania'),
(22, 'El Tunel', 'Ernesto Sabato', 'Novela Psicologica', '9788432248221', 3, 2, 'La obsesion y confesion del pintor Juan Pablo Castel'),
(23, 'Los de Abajo', 'Mariano Azuela', 'Novela Historica', '9789681602741', 4, 3, 'Cronica fundamental sobre la Revolucion Mexicana'),
(24, 'Fahrenheit 451', 'Ray Bradbury', 'Distopia', '9781451673319', 5, 4, 'Una sociedad del futuro donde los libros estan prohibidos'),
(25, 'El Retrato de Dorian Gray', 'Oscar Wilde', 'Clasico', '9780141439570', 4, 2, 'La busqueda de la eterna juventud y la decadencia moral'),
(26, 'La Tregua', 'Mario Benedetti', 'Novela', '9788420655475', 5, 2, 'El diario de Martin Santome y su inesperado romance'),
(27, 'Un Mundo Feliz', 'Aldous Huxley', 'Distopia', '9780060850524', 4, 3, 'Una sociedad perfecta controlada por la tecnologia y el consumo'),
(28, 'Metamorfosis', 'Franz Kafka', 'Ficcion Absurda', '9788420651361', 3, 2, 'La historia de Gregorio Samsa al amanecer transformado en insecto'),
(29, 'El Alquimista', 'Paulo Coelho', 'Narrativa', '9780062315007', 6, 5, 'El viaje de Santiago en busca de su leyenda personal'),
(30, 'El Hobbit', 'J.R.R. Tolkien', 'Fantasia', '9780345339683', 5, 4, 'Las aventuras de Bilbo Bolson y el viaje hacia la Montana Solitaria');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamo`
--

CREATE TABLE `prestamo` (
  `id_prestamo` int(11) NOT NULL,
  `matricula` varchar(20) NOT NULL,
  `titulo_libro` varchar(150) NOT NULL,
  `nombre_prestamista` varchar(100) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `prestamo`
--

INSERT INTO `prestamo` (`id_prestamo`, `matricula`, `titulo_libro`, `nombre_prestamista`, `fecha`) VALUES
(1, '', '1984', 'leonardo', '0000-00-00 00:00:00'),
(3, '', 'cien años de soledad', 'Maria', '2026-05-19 20:39:10'),
(4, '', 'el principito', 'Pedro', '2026-05-19 20:40:25'),
(5, '', 'el principito', 'Mariana', '2026-05-19 20:41:03'),
(9, '', '1984', 'leon', '2026-05-19 21:22:49'),
(10, '', '1984', 'Juanito', '2026-05-19 21:43:14'),
(15, '', 'paula', 'leonardo nuñez', '2026-05-20 08:10:56'),
(18, '', 'el cuaderno de maya', 'Lizeth', '2026-05-20 20:27:14'),
(21, '183782', 'frankenstein', 'Leonardo Núñez', '2026-05-24 02:58:22'),
(22, '183782', 'la tregua', 'Leonardo Núñez', '2026-05-24 04:00:44'),
(105, '180010', 'Don Quijote de la Mancha', 'Juan Hernández', '2026-05-24 07:04:42'),
(112, '180010', 'La Sombra del Viento', 'Juan Hernández', '2026-05-24 07:12:31'),
(113, '180010', 'El Amor en los Tiempos del Colera', 'Juan Hernández', '2026-05-24 07:12:31'),
(114, '180010', 'El Retrato de Dorian Gray', 'Juan Hernández', '2026-05-24 07:12:31'),
(115, '180010', 'La Tregua', 'Juan Hernández', '2026-05-24 07:12:31'),
(116, '180010', 'El Alquimista', 'Juan Hernández', '2026-05-24 07:12:31'),
(117, '180010', 'El Hobbit', 'Juan Hernández', '2026-05-24 07:12:31'),
(118, '183375', 'La Casa de los Espiritus', 'Maribel Aguilar', '2026-05-24 07:16:25'),
(120, '183375', 'Rayuela', 'Maribel Aguilar', '2026-05-24 07:19:33'),
(122, '183375', 'Dune', 'Maribel Aguilar', '2026-05-24 07:19:33'),
(127, '183375', 'Arrancame la Vida', 'Maribel Aguilar', '2026-05-24 07:20:30'),
(128, '183375', 'Del Amor y Otros Demonios', 'Maribel Aguilar', '2026-05-24 07:20:30'),
(129, '183375', 'El Cuaderno de Maya', 'Maribel Aguilar', '2026-05-24 07:20:48'),
(130, '183375', 'Ficciones', 'Maribel Aguilar', '2026-05-24 07:24:30'),
(131, '183375', 'Frankenstein', 'Maribel Aguilar', '2026-05-24 07:24:30'),
(132, '183375', 'Fahrenheit 451', 'Maribel Aguilar', '2026-05-24 07:24:30'),
(133, '183375', 'Un Mundo Feliz', 'Maribel Aguilar', '2026-05-24 07:24:30'),
(134, '183375', 'Metamorfosis', 'Maribel Aguilar', '2026-05-24 07:24:30'),
(135, '183375', 'Como Agua para Chocolate', 'Maribel Aguilar', '2026-05-24 07:26:33'),
(136, '183375', 'Pedro Paramo', 'Maribel Aguilar', '2026-05-24 07:26:33'),
(137, '183375', 'El Amor en los Tiempos del Colera', 'Maribel Aguilar', '2026-05-24 07:26:46'),
(138, '183375', 'El Tunel', 'Maribel Aguilar', '2026-05-24 07:26:46'),
(139, '183375', 'Los de Abajo', 'Maribel Aguilar', '2026-05-24 07:31:18'),
(140, '183375', 'El Retrato de Dorian Gray', 'Maribel Aguilar', '2026-05-24 07:31:18'),
(141, '183375', 'La Tregua', 'Maribel Aguilar', '2026-05-24 07:31:18'),
(142, '183375', 'El Principito', 'Maribel Aguilar', '2026-05-24 07:32:03');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `devolucion`
--
ALTER TABLE `devolucion`
  ADD PRIMARY KEY (`id_devolucion`);

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`id_estudiante`),
  ADD UNIQUE KEY `matricula` (`matricula`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `historial`
--
ALTER TABLE `historial`
  ADD PRIMARY KEY (`id_historial`);

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id_libro`);

--
-- Indices de la tabla `prestamo`
--
ALTER TABLE `prestamo`
  ADD PRIMARY KEY (`id_prestamo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administradores`
--
ALTER TABLE `administradores`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `devolucion`
--
ALTER TABLE `devolucion`
  MODIFY `id_devolucion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=82;

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `id_estudiante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `historial`
--
ALTER TABLE `historial`
  MODIFY `id_historial` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `prestamo`
--
ALTER TABLE `prestamo`
  MODIFY `id_prestamo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=143;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
