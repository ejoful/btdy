-- phpMyAdmin SQL Dump
-- version 4.7.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: 2017-07-23 17:49:00
-- 服务器版本： 5.5.55-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `btbtdy`
--
CREATE DATABASE IF NOT EXISTS `btbtdy` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `btbtdy`;

-- --------------------------------------------------------

--
-- 表的结构 `tbl_download`
--

DROP TABLE IF EXISTS `tbl_download`;
CREATE TABLE `tbl_download` (
  `id` int(11) UNSIGNED NOT NULL,
  `film_id` int(11) NOT NULL COMMENT '电影id',
  `name` varchar(255) NOT NULL COMMENT '名字',
  `size` varchar(255) NOT NULL COMMENT '文件大小',
  `type` varchar(255) DEFAULT NULL COMMENT '类型',
  `download_url` varchar(255) DEFAULT NULL COMMENT '下载地址',
  `position` tinyint(3) DEFAULT NULL COMMENT '排序',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tbl_download`
--

INSERT INTO `tbl_download` (`id`, `film_id`, `name`, `size`, `type`, `download_url`, `position`, `create_time`, `update_time`) VALUES
(1, 1, '星际穿越', '8.21GB', '720p', 'magnet:?xt=urn:btih:9ce598aa2eb2611eff6f110bf2bfa9430fb92424', 1, NULL, NULL),
(2, 1, '星际穿越', '8.7GB', '720p', 'magnet:?xt=urn:btih:9472a401f2fe04e071466a42860d4809961a878c', 2, NULL, NULL),
(3, 1, '星际穿越', '9.4GB', '720p', 'magnet:?xt=urn:btih:6ce397cb28b7f4bf13f2285caba3e2f5ef5d9a06', 3, NULL, NULL),
(4, 1, '星际穿越', '10.1GB国粤双语IMAX版', '720p', 'magnet:?xt=urn:btih:d977c108cd3a96d5246f458c96257868b246f81a', 4, NULL, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `tbl_film`
--

DROP TABLE IF EXISTS `tbl_film`;
CREATE TABLE `tbl_film` (
  `film_id` int(11) UNSIGNED NOT NULL,
  `name` varchar(255) DEFAULT NULL COMMENT '名字',
  `play_time` year(4) DEFAULT NULL COMMENT '年代（出品时间）',
  `update_time` timestamp NULL DEFAULT NULL COMMENT '更新',
  `quality` varchar(255) DEFAULT NULL COMMENT '清晰度',
  `type` varchar(255) DEFAULT NULL COMMENT '类型',
  `category` varchar(255) DEFAULT NULL COMMENT '分类',
  `location` varchar(255) DEFAULT NULL COMMENT '地区',
  `language` varchar(255) DEFAULT NULL COMMENT '语言',
  `imdb` varchar(255) DEFAULT NULL,
  `star` varchar(255) DEFAULT NULL COMMENT '主演',
  `descr` text COMMENT '剧情介绍',
  `list_pic` varchar(255) DEFAULT NULL COMMENT '列表页面图片',
  `detail_pic` varchar(255) DEFAULT NULL COMMENT '详细页面图片',
  `album` varchar(255) DEFAULT NULL COMMENT '相册',
  `short_video_url` varchar(255) DEFAULT NULL COMMENT '预告链接',
  `short_video_embed` text COMMENT '嵌入视屏代码',
  `subtitle` varchar(255) DEFAULT NULL COMMENT '字幕',
  `score` float DEFAULT NULL COMMENT '评分',
  `url` varchar(255) DEFAULT NULL COMMENT '链接'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tbl_film`
--

INSERT INTO `tbl_film` (`film_id`, `name`, `play_time`, `update_time`, `quality`, `type`, `category`, `location`, `language`, `imdb`, `star`, `descr`, `list_pic`, `detail_pic`, `album`, `short_video_url`, `short_video_embed`, `subtitle`, `score`, `url`) VALUES
(1, '星际穿越', 2014, '2016-01-01 07:52:00', '高清', '电影', '科幻 悬疑 冒险', '欧美', '英语', '未知', '马修·麦康纳 安妮·海瑟薇 杰西卡·查斯坦 韦斯·本特利 卡西·阿弗莱克 迈克尔·凯恩', '在不远的未来，随着地球自然环境的恶化，人类面临着无法生存的威胁。这时科学家们在太阳系中的土星附近发现了一个虫洞，通过它可以打破人类的能力限制，到更遥远外太空寻找延续生命希望的机会。一个探险小组通过这个虫洞穿越到太阳系之外，他们的目标是找到一颗适合人类移民的星球。在这艘名叫做“Endurance”的飞船上，探险队员着面临着前所未有，人类思想前所未及的巨大挑战。\r\n\r\n　　然而，通过虫洞的时候，他们发现飞船上的一个小时相当于地球上的七年时间，即使探险小组的任务能够完成，他们的救赎对于对地球上现在活着的人来说已经是太晚。飞行员库珀（马修·麦康纳饰演）必须在与自己的儿女重逢以及拯救人类的未来之间做出抉择。', 'http://gif-china.cc/uploads/litimg/201601/5d3d92fc8dc5ba41.jpg?h=250', NULL, '', NULL, NULL, 'http://subhd.com/search/%E6%98%9F%E9%99%85%E7%A9%BF%E8%B6%8A', 9, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_download`
--
ALTER TABLE `tbl_download`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_film`
--
ALTER TABLE `tbl_film`
  ADD PRIMARY KEY (`film_id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `tbl_download`
--
ALTER TABLE `tbl_download`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- 使用表AUTO_INCREMENT `tbl_film`
--
ALTER TABLE `tbl_film`
  MODIFY `film_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
