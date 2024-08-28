/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : book

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2024-06-12 00:04:00
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `admins`
-- ----------------------------
DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins` (
  `id` bigint(100) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL COMMENT '管理员账户',
  `password` varchar(100) NOT NULL COMMENT '管理员密码',
  `role` varchar(100) NOT NULL DEFAULT '1' COMMENT '管理员权限',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admins
-- ----------------------------
INSERT INTO `admins` VALUES ('1', 'admin', 'admin', '1');
INSERT INTO `admins` VALUES ('2', 'admins', 'admins', '1');

-- ----------------------------
-- Table structure for `bookinfo`
-- ----------------------------
DROP TABLE IF EXISTS `bookinfo`;
CREATE TABLE `bookinfo` (
  `id` bigint(100) NOT NULL AUTO_INCREMENT,
  `bookid` varchar(100) NOT NULL COMMENT '书号',
  `bookname` varchar(100) NOT NULL COMMENT '书名',
  `author` varchar(100) NOT NULL COMMENT '作者',
  `remaining` int(100) NOT NULL DEFAULT '1' COMMENT '书本数量',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of bookinfo
-- ----------------------------
INSERT INTO `bookinfo` VALUES ('1', '11101', 'PHP入门', 'aaa', '5');
INSERT INTO `bookinfo` VALUES ('13', '11102', 'python入门', 'bbb', '1');
INSERT INTO `bookinfo` VALUES ('14', '11103', 'css入门', 'ccc', '3');
INSERT INTO `bookinfo` VALUES ('15', '11104', 'html入门', 'ddd', '2');
INSERT INTO `bookinfo` VALUES ('16', '11105', '数据结构', 'eee', '1');
INSERT INTO `bookinfo` VALUES ('17', '11106', '机器学习', 'fff', '5');
INSERT INTO `bookinfo` VALUES ('18', '11107', 'javascript入门', 'ggg', '2');
INSERT INTO `bookinfo` VALUES ('19', '11108', '高等数学', 'hhh', '1');
INSERT INTO `bookinfo` VALUES ('20', '11109', 'web安全', 'iii', '3');
INSERT INTO `bookinfo` VALUES ('21', '11110', 'MySQL数据库', 'jjj', '1');
INSERT INTO `bookinfo` VALUES ('22', '11111', 'centos操作系统', 'kkk', '3');

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` bigint(100) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL DEFAULT '' COMMENT '账号',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `role` varchar(100) NOT NULL DEFAULT '0' COMMENT '0普通用户，1管理员',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('14', '1', '1', '0');
INSERT INTO `users` VALUES ('15', 'lin', '123', '0');
INSERT INTO `users` VALUES ('18', '6', '6', '0');
INSERT INTO `users` VALUES ('19', '666', '123', '0');

-- ----------------------------
-- Table structure for `usersborrow`
-- ----------------------------
DROP TABLE IF EXISTS `usersborrow`;
CREATE TABLE `usersborrow` (
  `id` bigint(100) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL COMMENT '用户名',
  `borrow` varchar(200) NOT NULL COMMENT '借用教室',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of usersborrow
-- ----------------------------
INSERT INTO `usersborrow` VALUES ('5', '2', '11104');
INSERT INTO `usersborrow` VALUES ('6', '2', '11101');
INSERT INTO `usersborrow` VALUES ('7', '2', '11102');
INSERT INTO `usersborrow` VALUES ('8', '3', '11101');
INSERT INTO `usersborrow` VALUES ('11', '3', '11104');
