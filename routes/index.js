var express = require('express');
var router = express.Router();
var axios = require('axios');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/hero', async function(req, res, next) {
  const res1 = await axios.get('https://lol.qq.com/biz/hero/champion.js');
  const hero = res1.data.split('if(!LOLherojs)var LOLherojs={};LOLherojs.champion=')[1]
  res.json(JSON.parse(hero.substr(0, hero.length-1)))
})

router.get('/hero/:name', async function(req, res, next) {
  const {name} = req.params;
  const res1 = await axios.get(`https://lol.qq.com/biz/hero/${name}.js`);
  const heroDetail = res1.data.split(`if(!LOLherojs)var LOLherojs={champion:{}};LOLherojs.champion.${name}=`)[1];
  res.json(JSON.parse(heroDetail.substr(0, heroDetail.length-1)))
})

module.exports = router;
