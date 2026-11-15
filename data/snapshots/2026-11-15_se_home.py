"""Sweden home & family snapshot, captured 2026-11-15 (Europe/Stockholm).

Real listings read from public Swedish outlet pages, with the product URL and
the product image URL exactly as published by the retailer. Nothing invented.
Booztlet (official Boozt outlet): all items unused, previous seasons.
The North Face SE outlet: new items at outlet price.
Run this file to write 2026-11-15_se_home.json (ingested by manual_snapshot).
"""
import json
import pathlib

OBS = "2026-11-15T18:20:00+01:00"
BZ = "https://www.booztlet.com/se/sv/"


def bimg(path, ver):
    q = f"has_webp=1&version={ver}&size=w400" if ver else "has_webp=1&size=w400"
    return f"https://image-resizing.booztcdn.com/{path}?{q}"


# (title, brand, price, regular, url path, image path, image version)
BOOZTLET = {
 "appliances": [
  ("Espresso Machine 7-in-1 Steel 20 Bar 1350W", "Hâws", 1499.50, 2999, "haws/espresso-machine-7-in-1-steel-20-bar-1350w_32991489/231453429", "haws/whs30cme5010_cblack.webp", "cbc955f1d9927b6a1b75851f82c3c124"),
  ("Sejerø 2.0 Double Air Fryer 2x4.5L 2400W", "Hâws", 1199.60, 2999, "haws/sejero-2-0-double-air-fryer-2x4-5l-2400w-pfas-free-coating_32991485/231453425", "haws/whs30afry30900_cblack_1.webp", "37d010e4232923e335af8ef98be9f02f"),
  ("Satisfry Air & Grill Multicooker", "Russell Hobbs", 1499.25, 1999, "russell-hobbs/satisfry-air-grill-multicooker_32786095/229237381", "russell-hobbs/rhs25030036001_cblack.webp", "e2e15c1b09cf6c0879cd37438403d7dd"),
  ("Elite Mix Stick Mixer", "OBH Nordica", 506.35, 779, "obh-nordica/elite-mix-stick-mixer_32170219/226155910", "obh-nordica/ona7715_cblack.webp", "560ac37d837d13c4222646d2384477f2"),
  ("Water Kettle Color LED 2200W", "Hâws", 449.50, 899, "haws/haws-water-kettle-color-led-2200w_33163046/233060734", "haws/whs30wkl29_cblack.webp", "12173859ed0f18aab444c45c8b756a69"),
  ("Espresso Machine 7-in-1 20 Bar 1350W", "Hâws", 1619.40, 2699, "haws/haws-espresso-machine-7-in-1-20-bar-1350w_33163154/233060918", "haws/whs30cme5082_cblack.webp", "5a466b1e8898782ee914d28d6c4ed2bf"),
  ("Stavmixer Maxx", "Bamix", 2804.15, 3299, "bamix/handblender-maxx-350-watt_32311574/226597348", "bamix/bax26519_cblack.webp", "4c5820dcec413fc5d82582065819e6f5"),
  ("Fresh & Save vakuum startset glas 7 delar", "Zwilling", 839.30, 1199, "zwilling-electricals/fresh-save-vacuum-starter-set-glass_32021817/225872813", "zwilling-electricals/zes1002503_cwhite.webp", "a31d1d53f012602c8a86d637de3d10fb"),
  ("Glöggkanna med värmare naturvit", "ERNST", 479.20, 599, "ernst/jug-and-heater-for-hot-drinks_32717205/228589393", "ernst/ert246762_cnaturalwhite.webp", "6c89c20166e9a1ef8c5e1c7dd6490b87"),
 ],
 "kitchen": [
  ("Asama knivset 3 delar", "Dorre", 399.60, 999, "dorre/asama-3-set-chef-s-knife-20-cm-santoku-18-cm-utility-knife-13-cm-_33059501/232102480", "dorre/doe59223_csilver.webp", "19d5ad1d6b56492bc6572e59264fae59"),
  ("Eminence stekpanna Ø30 cm", "Dorre", 449.50, 899, "dorre/eminence-frying-pan-30-cm_32873456/230187036", "dorre/doe59152_csilver.webp", "369d7dcef6e5d2f990064cb83202f4ef"),
  ("Kosmo gryta 10,1 liter", "Dorre", 521.95, 949, "dorre/kosmo-pot-with-lid-10-1-liters_32873454/230187032", "dorre/doe59150_csilver.webp", "91613014351fb3453cbe1bfcef7ca3b5"),
  ("Knivset Pluton 3 delar", "Lion Sabatier", 599.60, 1499, "lion-sabatier/knife-set-pluton-3-pack_31441819/225321365", "lion-sabatier/lsr20533_csteelblack.webp", "c3de4eec56eacb4712c530b276b089dc"),
  ("Wok Excellence Carbon", "Ken Hom", 539.40, 899, "ken-home/wok-excellence-carbon-ken-hom_28500711/222513749", "ken-home/khekh436003_csteel.webp", "bdb3f55e1b577ed163e4c03119fc3606"),
  ("Easy Chef stekpanna 24 cm", "Tefal", 374.25, 499, "tefal/easy-chef-frypan-24-cm_32170270/226155965", "tefal/tefg2700423_cgrey.webp", "2cee26d4e541c7dfe4500b3dc4cab22b"),
  ("Stekpanna gjutjärn", "Skottsberg", 725.40, 1209, "skottsberg/frypan-cast-iron-skottsberg_32613230/227637858", "skottsberg/skts531087_cblack.webp", "62a9baf78e96558761dcca013b3eaeed"),
  ("Nakiri 17 cm", "Miyabi", 2279.25, 3039, "miyabi/nakiri-17-cm_29166916/223102538", "miyabi/miy1002146_csilverblack.webp", "6172581df3a1b6fc40fb0f51a761ea91"),
  ("Skålset 6 delar New Margrethe", "Rosti", 486.85, 749, "rosti/mixing-bowl-set-6-parts-new-margrethe_32320981/226644188", "rosti/ros29948_chumus.webp", "2965e3e2dc48402db1ebce14ad99f25d"),
  ("Stekpanna 26 cm", "Greenpan", 719.40, 1199, "greenpan/frypan-26cm_33043976/231973539", "greenpan/gre04cw002318002_cblack.webp", "3a50022729cf549fa955a97ee7e796bd"),
  ("Skärbräda marmor", "Au Maison", 287.60, 719, "au-maison/marble-cutting-board_32615153/227656950", "au-maison/amnau90099203_cforestbrown.webp", "561336d317d919efa8510eda6ca93374"),
  ("Gryta Amandine", "Tareq Taylor", 479.50, 959, "tareq-taylor/casserole-amandine_32308626/226584896", "tareq-taylor/taq25432_csteel.webp", "d0e186936f59bfa6e421a91932dede7e"),
  ("Knivset Licorne 3 delar", "Lion Sabatier", 939.60, 2349, "lion-sabatier/knife-set-licorne-3-pack_31441848/225321394", "lion-sabatier/lsr20873_csteelblack_v1.webp", "9623939edeb6b0643fe1f76aa2163dfb"),
  ("Grytset med avtagbart handtag", "Holm", 359.40, 599, "holm/cookware-set-removable-handle_33217640/233416031", "holm/hho34115_cblack.webp", "4c0c4da629844b9efdace6869ec9e4af"),
  ("Martim salt- och pepparkvarn", "Bloomingville", 414.50, 829, "bloomingville/martim-salt-pepper-mill-black-rubberwood_33021657/231785708", "bloomingville/blo82061968_cblack_vset.webp", "f06d1ab8725fd914127467da60231d90"),
 ],
 "furniture": [
  ("Division hylla", "Andersen Furniture", 1066.45, 1939, "andersen-furniture/division_32942350/231026234", "andersen-furniture/afe4424070_cblack.webp", "380f88a3be4729eb8f2b60c1a80332ab"),
  ("Golvspegel Bubbly S", "Byon", 479.60, 1199, "byon/mirror-bubbly-s_33006982/231634958", "byon/byo5299001706_cbordeaux.webp", "f78111740580d48ebaa09ff37fa10a1c"),
  ("Skrivbord till hyllsystem Fari", "house doctor", 1330, 3800, "house-doctor/desk-for-shelving-system-fari-grey_32519648/227383676", "house-doctor/hdr208580365_cgrey.webp", "d76a50eb75a9daf7224df98b8fdbd11e"),
  ("Nooka loungebänk pappersrep", "Hâws", 1079.70, 3599, "haws/haws-nooka-lounge-bench-paper-cord_33163192/233060956", "haws/whs30hnbp_cnatural.webp", "c035abfd86a20fc9297817258b1e4e00"),
  ("Bokhylla", "house doctor", 550, 1100, "house-doctor/book-shelf_29210069/223128530", "house-doctor/hdr208580901_cblack.webp", "1d2abc2f98648e56c95616813a1db65e"),
  ("Bjørk bänk med förvaring, ekutseende", "House Nordic", 1312.80, 1750.40, "house-nordic-aps/bjork-bench-with-storage-oak-look-92x33x48-cm_32977015/231281095", "house-nordic-aps/hoo1401120_cnatural.webp", "0d2e661d244cfc05428c29d4985af879"),
  ("Klädhängare Rack svart", "house doctor", 595, 850, "house-doctor/rack-coat-rack_29210502/223128980", "house-doctor/hdr205850910_cblack_v1055169658.webp", "407aeffbb65bcccedd86f2c317867d78"),
  ("Rasa hylla 5 hyllplan, vit", "House Nordic", 1066.65, 1422.20, "house-nordic-aps/shelf_32775924/229151675", "house-nordic-aps/hoo3001071_cwhite.webp", "4358207f5d3759edc61c14d469a5d9d9"),
  ("Fåtölj bouclé vit/svart", "J-Line", 1599.50, 3199, "j-line/loun-cha-bouc-ply-poly-whi-bla_33087158/232309670", "j-line/jln50853_cwhite.webp", "d6893d874081c93bc53d7f048358b0f9"),
  ("Moa väggspegel 70x100 cm", "House Nordic", 902.55, 1203.40, "house-nordic-aps/moa-wall-mirror-organic-shape-facet-70x100-cm_32977009/231281089", "house-nordic-aps/hoo4001091_cclear.webp", "c64635bc308048751a87942321d3c62f"),
  ("Ever väggspegel", "Muubs", 1214.50, 2429, "muubs/ever-mirror_29640792/223629170", "muubs/muu9010002053_cblack.webp", "1ad4b9840a5ecb96f661eb650f96659f"),
  ("Hazem skåp", "Bloomingville", 1439.40, 2399, "bloomingville/hazem-cabinet_33072164/232195724", "bloomingville/blo82069617_cred.webp", "1399e57d4e3a721e5ac6a1e88f882d91"),
  ("Stol Viejo", "Leitmotiv", 314.50, 629, "leitmotiv/chair-viejo_33075517/232227722", "leitmotiv/leilm2362gy_cgrey_v1.webp", "17e2ae79e4d291eafb434fc7d079feee"),
  ("Manhatten hylla", "Muubs", 1291.60, 3229, "muubs/manhatten_32639345/227923275", "muubs/muu9190002205_cblack.webp", "fe5d35a0f836e4ac93c94bbb1580126b"),
  ("Vitrinskåp glas", "house doctor", 2325, 3100, "house-doctor/glass-cabinet_29210271/223128741", "house-doctor/hdr203660763_cbrass_v1055169528.webp", "98b058d560651fdfe7cf79367fd24fae"),
  ("Matilda fåtölj", "House Nordic", 5021.25, 7725, "house-nordic-aps/selje-lounge-chair_33201461/233317083", "house-nordic-aps/hoo1101076_cbrown.webp", "47e075e4b62c870118aa3445223eba48"),
  ("Skoskåp Shoe Box Narrow, varm ek", "ReCollector", 2137.46, 2849.95, "recollector/shoe-box-narrow-warm-oak_33177553/233152355", "recollector/recr417862_cwarmoak.webp", "3790672ca8f2c6d592dcc30c2a78a86b"),
  ("Soffbord Force", "Leitmotiv", 1799.25, 2399, "leitmotiv/table-force_32969119/231233938", "leitmotiv/leilm2152_cbrown.webp", "e8bf461e4aafdf71c17e9b0c4b68c1e9"),
  ("Nora matstol ask", "House Nordic", 1684.76, 2406.80, "house-nordic-aps/counter-chair_32776020/229151747", "house-nordic-aps/hoo1001380_cnaturebrownblack_4.webp", "55603ea432453debdf84b01adeba0c23"),
  ("Element sidobord", "Novoform", 1399.50, 2799, "novoform/element-table_29642106/223633770", "novoform/noonov800200_cblack.webp", "6d1138487f6aedb96cd506184ff26d7d"),
  ("Serveringsvagn Roll bordeaux", "house doctor", 1500, 2000, "house-doctor/trolley-hdroll-burgundy_32874761/230192707", "house-doctor/hdr208580321_cburgundy_v2016134337.webp", "c0287f6e077c0f702f51c42259149cf2"),
  ("Pall vit", "Nichba Design", 1999.50, 3999, "nichba-design/stool_28857256/222863391", "nichba-design/chbl100114w_cwhite.webp", None),
 ],
 "home_textiles": [
  ("Sängöverkast bomull med lin och fransar", "C'est Bon", 1034.55, 2299, "cest-bon/bedspread-cotton-w-linentassels_29333839/223263145", "cest-bon/cbncb16199802_clinen.webp", "5524d12dedcc8a67a5387b6749043fad"),
  ("Unikko duk 140x250 cm", "Marimekko Home", 840, 2100, "marimekko-home/unikko-jacq-table-c-140x250cm_32767819/229088044", "marimekko-home/mhe072564_coffwhite.webp", "4d39ff89a905f841fdc68c8b7dde41b8"),
  ("Pläd Ponra", "house doctor", 319.60, 799, "house-doctor/throw-ponra_32518185/227376875", "house-doctor/hdr201600030_cgrey.webp", "8c6d75664fb9bc1bd8614db70f036812"),
  ("Volano matta bomull", "Bloomingville", 741.95, 1349, "bloomingville/volano-rug_32748125/228926111", "bloomingville/blo82062123_cnature.webp", "bd06a94b53deb12d5d67338e2817396f"),
  ("Stickad pläd 160x130 cm", "Ceannis", 494.45, 899, "ceannis/knitted-throw-160x130cm_32489154/227230162", "ceannis/cea050421626_cbeige.webp", "38e8c86aa786ecc3b1e3831ca5c9f1c5"),
  ("Iso Räsymatto påslakanset 150x210", "Marimekko Home", 625, 1250, "marimekko-home/iso-r-symatto-set150x210-50x60_33184082/233197190", "marimekko-home/mhe076163_coffwhitecharcoal.webp", "73e03b8143108963a6fdc52840d7809c"),
  ("Bæk&Bølge påslakanset 220x220 cm", "Juna", 689.70, 2299, "juna/baek-bolge-bed-linen-220x220-cm-green-light-blue-se_32701267/228406700", "juna/na637123_cgreenlightblue.webp", "caef45d502e83d3e4ad1d83d317022e6"),
  ("Pläd 140x200 khakigrön", "Sekan Studio", 449.70, 1499, "sekan-studio/plaid-140x200-khaki-green_32978629/231291011", "sekan-studio/skur06342_ckhakigreen.webp", "f556ed62d6bc6d7a814dec9a219c178e"),
  ("Ullfilt", "humble LIVING", 449.50, 899, "humble-living-blankets/wool-blanket-humble-living_32950090/231072498", "humble-living-blankets/hlbbzthlb25311color_csimplytaupe.webp", "3b21d7e6bb2bfbae7435815c53e3db7f"),
  ("Handdukspaket 12 st antracit", "Sekan Studio", 1049.70, 3499, "sekan-studio/towel-bundle-set-of-12-antracit_33101772/232435716", "sekan-studio/sku26toantracit5_cantracit.webp", "1b96be0c366fcf3bf4a69626b22227ee"),
  ("Drottningholm pläd", "LINUM", 599.70, 1999, "linum/drottningholm-throw_29933590/223950603", "linum/num17dro23700_ccamelbrown.webp", "bd62417bc142abcb5ecb07b7a982f3f6"),
  ("Oxford ullpläd 140x240 cm", "Silkeborg Uldspinderi", 1750, 3500, "silkeborg-uldspinderi/oxford-140x240-cm_28493507/222506217", "silkeborg-uldspinderi/ilk001070_c5104shadesbrown.webp", None),
  ("Enjoy påslakanset", "Turiform", 639.60, 1599, "turiform/enjoy_32780286/231406494", "turiform/tur4002069_crose.webp", "ac69e934dccd7970da42cb4a46956790"),
  ("Sateen påslakan enkel", "Gant", 1020, 1700, "gant-clothing/sateen-single-duvet_32506283/227312108", "gant-clothing/gcl851029302_cmarine_v410.webp", "f9ae6ffa2139f7d17b47907682d43d70"),
 ],
 "shoes_women": [
  ("Response 2 W", "adidas Performance", 439.45, 799, "adidas/response-2-w_32918738/230710257", "adidas/adikj1767_cicepursilvmtbeaora.webp", "e7b038991fc0ae69f27af9b0841f6733"),
  ("Easy Going High Zip", "Skechers", 909.35, 1399, "skechers/womens-easy-going_27687085/212731401", "skechers/ske167108_cchocchocolate.webp", "3634e443816385cc919baf94848db91a"),
  ("Orinoco3 Top D", "Clarks", 974.35, 1499, "clarks/orinoco3-top-d_32888616/230349248", "clarks/clrcl26182901_cblackleather_v1216.webp", "7b74da6974ff0380772e67b964ec1f15"),
  ("Square Toe Leather Bootie", "Tommy Hilfiger", 759.60, 1899, "tommy-hilfiger-shoes/th-square-toe-leather-bootie_32887017/230331308", "tommy-hilfiger-shoes/thsfw0fw09046_cblack_vbds.webp", "82eabb6f71ba7b58d589a8b23d96f2f1"),
  ("Aino", "Vagabond", 900, 2000, "vagabond/aino_32751399/228947794", "vagabond/vga5829102_cblack.webp", "462d4ee650e5aeb9f7cf2ba3349413fd"),
  ("Constance", "Steve Madden", 1319.45, 2399, "steve-madden/constance-boots_32750329/228942040", "steve-madden/smn11003238_cblackleather.webp", "bee61366e913bb230616caed9cd597a5"),
  ("Alux Hybrid", "Tretorn", 910, 1400, "tretorn/alux-hybrid_28584021/222646002", "tretorn/tre473434_c010black_v010.webp", "51da32b107324f4919bb3675d58bff4d"),
  ("Biom 720 W", "ECCO", 1209.45, 2199, "ecco/biom-720-w_32919381/230716900", "ecco/ec850303_c854881228_v57019.webp", "7398cb4c60c06e2cafcd47cb54b6de7f"),
  ("Fallwi Mid Boot", "Gant", 1039.60, 2599, "gant/fallwi-mid-boot_32889283/230354306", "gant/gan31541129_cdarkbrown_vnolength_4.webp", "6414bbd63a3314fd80d999a79e0f84ac"),
  ("UA Old Skool", "Vans", 449.50, 899, "vans/ua-old-skool_32480848/20723034", "vans/vanvn0a4bv51951_cpewtertruewhite_vvn195.webp", "7a4c6ccea8a4268a692f25d266fc1230"),
  ("Gazelle", "adidas Originals", 674.50, 1349, "adidas-originals/gazelle_32622262/18492721", "adidas-originals/adib41645_ccburguftwwhtgoldmt.webp", "01ad29019de2faf749bd9ba7b2c9231a"),
  ("Campus 00s W", "adidas Originals", 724.50, 1449, "adidas-originals/campus-00s-w_32816641/229578452", "adidas-originals/adijq8292_caurplucwhitegum3.webp", "5160b836f67b6e3dd94116adf3ae5af5"),
  ("Arch Hybrid Wool Ice.Ctrl W", "Tretorn", 1235, 1900, "tretorn/arch-hybrid-wool-ice-ctrl-w_32637565/227914755", "tretorn/tre800651_c059black_v059.webp", "732159cc30bc7ec2ae94e9dd7d391027"),
  ("Jam Electric", "Nike", 749.50, 1499, "nike-booztlet-new/wmns-jam-electric_32977645/231285190", "nike-booztlet-new/niefn0314_c2296719756.webp", "976bcdde2ff24c93c659bd38e11f7099"),
  ("57/40 Animal Print", "New Balance", 930, 1550, "new-balance/new-balance-57-40_31438237/225300547", "new-balance/nbaw5740apa_cblack_vw5740apabla.webp", "baa0c0514042345d10f516b516624ee7"),
  ("KNX Lace W", "KEEN", 880, 1600, "keen/ke-knx-lace_32831618/229732232", "keen/kee7051028355_cblackstarwhite.webp", "85dc9e8150bb6b118f28b77df316c49d"),
 ],
 "shoes_men": [
  ("Hylane", "Vans", 629.40, 1049, "vans/hylane_32923844/230771713", "vans/vanvn000d1jflr1_cyellowdust_vvnflr.webp", "df1eaf9e99bf9fcbd42ffb0bb62be500"),
  ("Mike loafers", "Vagabond", 1235, 1900, "vagabond/mike_33082320/232281035", "vagabond/vga5263101_cblack.webp", "bad23f43ecf43fcf715cff6d857c0812"),
  ("Campus 00s", "adidas Originals", 796.95, 1449, "adidas-originals/campus-00s_31325182/225108643", "adidas-originals/adih03472_cdrkgrnftwwhtowhite.webp", "1bd2d062790a96bd494de4cdb6bf514c"),
  ("Kieran Hito kängor", "BOSS", 1364.35, 2099, "boss-black/kieran-hito-altb_33016647/231736189", "boss-black/bob50555274_cblack_v005.webp", "254a0a65feeae5aefa79055604aae8d9"),
  ("Jay monks", "Vagabond", 1440, 2400, "vagabond/jay_32944991/231045234", "vagabond/vga6077001_cblack.webp", "d9839aa30cfa31b106063ab8bff9f7b7"),
  ("The Roger Advantage", "On", 1235, 1900, "on-running/the-roger-advantage_33000274/230915139", "on-running/org3mf30641043_cblackblack.webp", "06a52fbd79669298ca856597afeabf0c"),
  ("City Chelsea Fleece WP M", "Viking", 780, 1300, "viking/city-chelsea-fleece-wp-m_32833122/229756426", "viking/vik395670_ccement.webp", "13b4229ead04752a5fff8259e81b97b3"),
  ("2002R", "New Balance", 1350, 1800, "new-balance/new-balance-2002r_32891898/230400204", "new-balance/nbau20028rg_cwoodland_vu20028rgwoo.webp", "9c798b7bdba656a6dde3b28c017b3892"),
  ("Chuck Taylor All Star", "Converse", 582, 970, "converse/chuck-taylor-all-star_32945580/231047383", "converse/cona13027c_ctotallyfudgedegret.webp", "48fa937409a2d8af5b63c09c0808a615"),
  ("Bradstreet", "Timberland", 1199.25, 1599, "timberland/bradstreet-advchk-md-brn-7-medium_18745529/18745560", "timberland/timtb0a13ee214_cbrown.webp", "1c34f87dc4309ab9186e9fa3b3de909e"),
  ("Blisdor Chelsea Boot", "Gant", 1374.45, 2499, "gant/blisdor-chelsea-boot_32877480/230212453", "gant/gan31651068_cblack_3.webp", "8ef280139ffa2b3319cb0e0092909fe9"),
  ("MB Moon247 X-Lace", "Moon Boot", 1200, 2400, "moon-boot/mb-moon247-xlace_32865415/230113856", "moon-boot/mbt80d2490100_cblack.webp", "8f517ddf52c9366acdaab859f30b5ea8"),
  ("Jenson Oxford svart läder", "Hush Puppies", 825, 1500, "hush-puppies/men-s-jenson-oxford-bold-black-leather_33020682/231777772", "hush-puppies/hpuhpm10607_cboldblackleather.webp", "088fa5f577e0d006c336210edc4e5454"),
  ("Ultrarun 5", "adidas Performance", 616.85, 949, "adidas/ultrarun-5_32725081/228680955", "adidas/adijs2836_cftwwhtcblackftwwht.webp", "32acd8b963586ea730f4ac65b5e5b75b"),
  ("GrandPro Luxe slip-on", "Cole Haan", 1481.35, 2279, "cole-haan/grandpro-luxe-slip-on-sneakers_33065654/232160039", "cole-haan/chnc43999_c23340099.webp", "09a9df212602f4959b15c7e6da1a6fc2"),
  ("Classic Slip-On", "Vans", 479.40, 799, "vans/classic-slip-on_30324940/10081160", "vans/vanvn000eyeblk1_cblack_vvnblk.webp", "efcc5e08d441a2618c0adce71ee61256"),
 ],
 "shoes_kids": [
  ("Aspen K vinterstövlar", "Exani", 209.70, 699, "exani/aspen-k_32885095/230318597", "exani/exa11352286_crust.webp", "431148ec52b5a38ccefac369b1fae93c"),
  ("Thermal Boot fodrade gummistövlar", "mikk-line", 246.35, 379, "mikkline/thermal-boot_33153492/233014057", "mikkline/mik38062_cfalcon.webp", "6345ff4e4f197736320dfa26fdc78b81"),
  ("Campus 00s J", "adidas Originals", 219.80, 1099, "adidas-originals/campus-00s-j_31324939/228581538", "adidas-originals/adiji0286_ccpurplpreyelftwwht.webp", "cc4a578e57b8836a3f980158f6b04f16"),
  ("Snow Mountain vinterstövlar", "ECCO", 899.25, 1199, "ecco/snow-mountain_32849659/229922994", "ecco/ec710322_c2461339270_v51642.webp", "50ece7bbae8827fa82e9bd6822bd991d"),
  ("Mimas Hybrid vinterstövlar", "Tretorn", 540, 900, "tretorn/mimas-hybrid_30309587/225195562", "tretorn/tre800237_c050jetblack_v050.webp", "d11f4aa4bfc5546dbe925baf606e3497"),
  ("Nuuk vinterstövlar", "PAX", 510, 850, "pax/nuuk-pax_32757113/229004534", "pax/pax7261224_cblack.webp", "b0884bd0fbecfe3717d77c3e5cec6821"),
  ("Storm Warm fodrade gummistövlar", "Viking", 490, 700, "viking/storm-warm_32833087/229755467", "viking/vik125300_cblack.webp", "69fa5bf727c3fa545fe5daec15bac349"),
  ("Icicle vinterstövlar", "Hummel", 360, 900, "hummel/icicle_32830734/229723377", "hummel/hu230881_cebony.webp", "415260299dcdec85a6bb7e261e16600a"),
  ("Mora WP vinterstövlar", "Kavat", 559.30, 799, "kavat/mora-wp_32753242/228968424", "kavat/kav61995242_cbrown.webp", "65136aed4bc609f321e8f847eeca40f8"),
  ("Snow Mountain svart", "ECCO", 520, 1300, "ecco/snow-mountain_32849658/229922983", "ecco/ec710332_cblacktarmac_v56665.webp", "087928e646e247c58e2f4f5d67d31f49"),
  ("Strada low kids", "FILA", 150, 750, "fila-footwear/strada-low-kids_27889138/21358618", "fila-footwear/fil1010781_cwhite_v1fg.webp", "5b365fdca4cc51a47c1ef75e7df55d55"),
  ("Thermal gummistövlar med ullfoder", "CeLaVi", 223.98, 559.95, "celavi-ob/thermal-wellies-w-wool-lining_32871885/230172918", "celavi-ob/ela320181_cbrickdust.webp", "4131ab4fff4fd421c777357905c7ad4d"),
 ],
}

TNF = "https://www.thenorthface.com/sv-se/p/"
TNFI = "https://assets.thenorthface.eu/images/t_img/"
# (title, price, regular, product path, image path after t_img/, category)
THE_NORTH_FACE = [
 ("Terra Peak Jacket M", 1099.50, 2199, "herr-211701/terra-peak-jacket-m-NF0A88U2?color=D1R", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1771926400/NF0A88U2D1R-HERO/Mens-Terra-Peak-Jacket-TNF-Estate-Blue-HERO.jpg", "clothing"),
 ("Aral Insulated Parka M", 2449.30, 3499, "herr-211701/aral-insulated-parka-m-NF0A8FQ7?color=8K2", "c_fill,ar_4:5,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1785165635/NF0A8FQ78K2-HERO/Mens-Aral-Insulated-Parka-TNF-Summit-Navy-HERO.jpg", "clothing"),
 ("Huila Synthetic Insulation Hooded Jacket M", 1379.40, 2299, "herr-211701/huila-synthetic-insulation-hooded-jacket-m-NF0A85A3?color=4GZ", "b_gen_fill,c_pad,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1788276715/NF0A85A34GZ-HERO/Mens-Huila-Synthetic-Insulation-Hooded-Jacket-TNF-TNF-BlackAsphalt-GreyNPF-HERO.jpg", "clothing"),
 ("Ridgelite Futurefleece Wind Jacket M", 1319.40, 2199, "herr-211701/ridgelite-futurefleece-wind-jacket-m-NF0A8ES6?color=JV4", "b_gen_fill,c_pad,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1788277882/NF0A8ES6JV4-HERO/Mens-Ridgelite-FUTUREFLEECE-Wind-Jacket-TNF-CedarNew-Taupe-Green-HERO.jpg", "clothing"),
 ("Huila Synthetic Insulation Jacket M", 1319.40, 2199, "herr-211701/huila-synthetic-insulation-jacket-m-NF0A85AE?color=2EL", "b_gen_fill,c_pad,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1788276715/NF0A85AE2EL-HERO/Mens-Huila-Synthetic-Insulation-Jacket-TNF-Cedar-HERO.jpg", "clothing"),
 ("Hybrid Tek Approach Full-Zip Hooded Jacket M", 1079.40, 1799, "herr-211701/hybrid-tek-approach-full-zip-hooded-jacket-m-NF0A8EUC?color=G7O", "b_gen_fill,c_pad,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1788277888/NF0A8EUCG7O-HERO/Mens-Hybrid-Tek-Approach-FullZip-Hooded-Jacket-TNF-Transcendent-Grey-HERO.jpg", "clothing"),
 ("Tansa Softshell Jacket M", 1079.40, 1799, "herr-211701/tansa-softshell-jacket-m-NF0A8G31?color=BRI", "b_gen_fill,c_pad,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1788278431/NF0A8G31BRI-HERO/Mens-Tansa-Softshell-Jacket-TNF-Woodland-Green-HERO.jpg", "clothing"),
 ("Sangro Jacket M", 1049.40, 1749, "herr-211701/sangro-jacket-m-NF00A3X5?color=BRI", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1771925979/NF00A3X5BRI-HERO/Mens-Sangro-Jacket-TNF-Woodland-Green-HERO.jpg", "clothing"),
 ("Descendit Trousers M", 1539.30, 2199, "herr-211701/descendit-trousers-m-NF0A87ZY?color=BQ1", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1774279844/NF0A87ZYBQ1-HERO/Mens-Descendit-Trousers-TNF-Slate-Moss-HERO.jpg", "clothing"),
 ("Tek Approach Jacket M", 959.40, 1599, "herr-211701/tek-approach-jacket-m-NF0A8B58?color=G7O", "b_gen_fill,c_pad,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1788277065/NF0A8B58G7O-HERO/Mens-Tek-Approach-Jacket-TNF-Transcendent-Grey-HERO.jpg", "clothing"),
 ("Red Box Totebag", 869.40, 1449, "vaskor-and-utrustning-211747/red-box-totebag-NF0A8EGE?color=21L", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1763487299/NF0A8EGE21L-HERO/Red-Box-Tote-Bag-TNF-New-Taupe-Green-HERO.jpg", "bags"),
 ("Rucksack Glen Canyon", 749.40, 1249, "vaskor-and-utrustning-211747/rucksack-glen-canyon-NF0A8EER?color=JV4", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1764251191/NF0A8EERJV4-HERO/Glen-Canyon-Rucksack-TNF-CedarNew-Taupe-Green-HERO.jpg", "bags"),
 ("Altamesa 300 Trail Running Shoes W", 779.40, 1299, "skor-747784/altamesa-300-trail-running-shoes-w-NF0A8A9S?color=4TO", "c_fill,ar_4:5,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1787580648/NF0A8A9S4TO-HERO/Womens-Altamesa-300-Trail-Running-Shoes-TNF-MauveMidnight-Mauve-HERO.jpg", "shoes_women"),
 ("Glenclyffe Shoe", 1169.40, 1949, "skor-747784/glenclyffe-shoe-NF0A8DAP?color=L1O", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1787737098/NF0A8DAPL1O-HERO/Glenclyffe-Shoes-TNF-High-Rise-GreyStone-Slab-HERO.jpg", "shoes_men"),
 ("Fastpack Waterproof Shoes W", 989.40, 1649, "dam-211718/fastpack-waterproof-shoes-w-NF0A8G5J?color=KH8", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1763143656/NF0A8G5JKH8-HERO/Womens-Fastpack-Waterproof-Shoes-TNF-HERO.jpg", "shoes_women"),
 ("Altamesa Trail Running Shoes Junior", 509.40, 849, "skor-747784/altamesa-trail-running-shoes-junior-NF0A83O4?color=73K", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1754054656/NF0A83O473K-HERO/Teens-Altamesa-Trail-Running-Shoes-TNF-HERO-BLUESULPHUR-SPRING-GREEN-HERO.jpg", "shoes_kids"),
 ("Offtrail GORE-TEX Hiking Boots W", 1469.30, 2099, "skor-747784/offtrail-gore-tex-hiking-boots-w-NF0A8AEU?color=GKP", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1763057306/NF0A8AEUGKP-HERO/Womens-Offtrail-GORETEX-Hiking-Boots-TNF-Frost-GreyGranite-Grey-HERO.jpg", "shoes_women"),
 ("VECTIV Fastpack Lite Hiking Shoes W", 1084.30, 1549, "dam-211718/vectiv-fastpack-lite-hiking-shoes-w-NF0A8AFC?color=CIR", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1759928596/NF0A8AFCCIR-HERO/Womens-VECTIV-Fastpack-Lite-Hiking-Shoes-TNF-ConcreteSmoked-Pearl-HERO.jpg", "shoes_women"),
 ("Offtrail TR GORE-TEX Trail Running Shoes M", 1224.30, 1749, "skor-747784/offtrail-tr-gore-tex-trail-running-shoes-m-NF0A8A9X?color=16Y", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1770146893/NF0A8A9X16Y-HERO/Mens-Offtrail-TR-GORETEX-Trail-Running-Shoes-TNF-Hero-BlueTNF-Black-HERO.jpg", "shoes_men"),
 ("Altamesa 300 V2 Trail Running Shoes M", 1231.65, 1449, "skor-747784/altamesa-300-v2-trail-running-shoes-m-NF0A8G6M?color=6S4", "c_pad,b_gen_fill,f_auto,h_240,e_sharpen:60,w_192/dpr_2.0/v1765810501/NF0A8G6M6S4-HERO/Mens-Altamesa-300-V2-Trail-Running-Shoes-TNF-CalacattaSoapstone-HERO.jpg", "shoes_men"),
]


IKEA_P = "https://www.ikea.com/se/sv/p/"
IKEA_I = "https://www.ikea.com/se/sv/images/products/"
# IKEA "Utgår inom kort" (last chance, discontinued). The page shows current price only,
# no previous price per product, so no discount is claimed. (title, price, product slug, image file, category)
IKEA_LAST_CHANCE = [
 ("RAMNEFJÄLL Klädd sängstomme, Kilanda ljusbeige/Luröy, 160x200 cm", 2195, "ramnefjaell-klaedd-saengstomme-kilanda-ljusbeige-luroey-s19552751", "ramnefjaell-klaedd-saengstomme-kilanda-ljusbeige-luroey__1258172_pe927371_s5.jpg", "furniture"),
 ("VIHALS Förvaringskombination, vit, 235x37x140 cm", 2990, "vihals-foervaringskombination-vit-s09440617", "vihals-foervaringskombination-vit__1079331_pe857502_s5.jpg", "furniture"),
 ("EKTORP 3-sitssoffa, Kilanda mörkblå", 5595, "ektorp-3-sitssoffa-kilanda-moerkbla-s29509007", "ektorp-3-sitssoffa-kilanda-moerkbla__1194843_pe902111_s5.jpg", "furniture"),
 ("JAKOBSFORS Soffbord, mörkbrun betsad ekfaner, 80 cm", 1195, "jakobsfors-soffbord-moerkbrun-betsad-ekfaner-50515167", "jakobsfors-soffbord-moerkbrun-betsad-ekfaner__1108164_pe869323_s5.jpg", "furniture"),
 ("SONGESAND Sängstomme, vit, 90x200 cm", 1295, "songesand-saengstomme-vit-80372553", "songesand-saengstomme-vit__0637618_pe698428_s5.jpg", "furniture"),
 ("BESTÅ Hylla med dörrar, svartbrun Hedeviken/mörkbrun betsad ekfaner, 120x42x64 cm", 2495, "besta-hylla-med-doerrar-svartbrun-hedeviken-moerkbrun-betsad-ekfaner-s49426153", "besta-hylla-med-doerrar-svartbrun-hedeviken-moerkbrun-betsad-ekfaner__1001175_pe824446_s5.jpg", "furniture"),
 ("VÅRKUMLA Bäddfåtölj, Vansta blå", 2995, "varkumla-baeddfatoelj-vansta-bla-80587704", "varkumla-baeddfatoelj-vansta-bla__1368599_pe957819_s5.jpg", "furniture"),
 ("STORJORM Spegel med integrerad belysning, vit, 80x60 cm", 1495, "storjorm-spegel-med-integrerad-belysning-vit-70248125", "storjorm-spegel-med-integrerad-belysning-vit__0637661_pe698451_s5.jpg", "furniture"),
 ("METOD Högskåp med skafferiutdrag, vit/Stensund vit, 60x60x220 cm", 8724, "metod-hoegskap-med-skafferiutdrag-vit-stensund-vit-s59472031", "metod-hoegskap-med-skafferiutdrag-vit-stensund-vit__1065201_pe852169_s5.jpg", "kitchen"),
 ("VARDAGEN Nudelsil, rostfritt stål/bok, 30 cm", 59, "vardagen-nudelsil-rostfritt-stal-bok-30581511", "vardagen-nudelsil-rostfritt-stal-bok__1300139_pe936974_s5.jpg", "kitchen"),
 ("UPPLAGA Assiett, vit, 22 cm", 39, "upplaga-assiett-vit-70424703", "upplaga-assiett-vit__0714567_pe730130_s5.jpg", "kitchen"),
 ("IDEALISK Tång, rostfritt stål", 29, "idealisk-tang-rostfritt-stal-70579375", "idealisk-tang-rostfritt-stal__1271529_pe929482_s5.jpg", "kitchen"),
 ("IKEA 365+ Kastrull, rostfritt stål, 1.0 l", 99, "ikea-365-kastrull-rostfritt-stal-00484229", "ikea-365-kastrull-rostfritt-stal__1006177_pe825762_s5.jpg", "kitchen"),
 ("ISTAD Återförslutningsbar påse, mönstrad/grön, 6/4.5 l", 49, "istad-aterfoerslutningsbar-pase-moenstrad-groen-40525685", "istad-aterfoerslutningsbar-pase-moenstrad-groen__1105120_pe868046_s5.jpg", "kitchen"),
 ("ÄNGSLILJA Påslakan 1 örngott, blågrå, 150x200/50x60 cm", 199, "aengslilja-paslakan-1-oerngott-blagra-70585220", "aengslilja-paslakan-1-oerngott-blagra__1316021_pe940602_s5.jpg", "home_textiles"),
 ("NÄSSELKLOCKA Påslakan 1 örngott, ljust gråbeige/flerfärgad, 150x200/50x60 cm", 249, "naesselklocka-paslakan-1-oerngott-ljust-grabeige-flerfaergad-10584544", "naesselklocka-paslakan-1-oerngott-ljust-grabeige-flerfaergad__1315020_pe940355_s5.jpg", "home_textiles"),
 ("DVALA Dra-på-lakan, ljusgrå, 90x200 cm", 99, "dvala-dra-pa-lakan-ljusgra-50482459", "dvala-dra-pa-lakan-ljusgra__0811765_pe771834_s5.jpg", "home_textiles"),
 ("SPETSBOJ Bordslampa, dimbar/grön, 22 cm", 149, "spetsboj-bordslampa-dimbar-groen-70591612", "spetsboj-bordslampa-dimbar-groen__1355495_pe953147_s5.jpg", "decor_lighting"),
 ("KRUSNATE Takspot med 2 spots, vit", 79, "krusnate-takspot-med-2-spots-vit-10562085", "krusnate-takspot-med-2-spots-vit__1198149_pe903922_s5.jpg", "decor_lighting"),
 ("SMYCKA Konstgjord blomma, inom-/utomhus/hortensia blå, 55 cm", 50, "smycka-konstgjord-blomma-inom-utomhus-hortensia-bla-10617686", "smycka-konstgjord-blomma-inom-utomhus-hortensia-bla__1485396_pe1001947_s5.jpg", "decor_lighting"),
 ("MORKULLA Doftljus i glas, Syren blandade färger, 12 tim.", 29, "morkulla-doftljus-i-glas-syren-blandade-faerger-60619598", "morkulla-doftljus-i-glas-syren-blandade-faerger__1485016_pe1001793_s5.jpg", "decor_lighting"),
 ("SKYNKE Bärkasse, blekgul/flerfärgad, 45x36 cm", 9, "skynke-baerkasse-blekgul-flerfaergad-20624785", "skynke-baerkasse-blekgul-flerfaergad__1457452_pe992643_s5.jpg", "bags"),
]


def build():
    out = []
    for cat, rows in BOOZTLET.items():
        for t, b, p, r, u, ip, v in rows:
            out.append(dict(source="booztlet_se", retailer="Booztlet", country="SE", currency="SEK",
                            title=t, brand=b, price=p, regular_price=r, category=cat,
                            condition="clearance",
                            condition_text="Outletvara, oanvänd. Tidigare säsong. / Outlet item, unused, previous season.",
                            url=BZ + u, url_kind="product", image_url=bimg(ip, v),
                            availability_text="Leverans 1-2 vardagar, från 49 kr. Retur 59 kr, 14 dagar.",
                            list_url=BZ, observed_at=OBS))
    for t, p, r, u, ip, cat in THE_NORTH_FACE:
        out.append(dict(source="thenorthface_se", retailer="The North Face", country="SE", currency="SEK",
                        title=t, brand="The North Face", price=p, regular_price=r, category=cat,
                        condition="clearance", condition_text="Outlet, ny vara. / Outlet, new item.",
                        url=TNF + u, url_kind="product", image_url=TNFI + ip,
                        availability_text="Online, leverans i Sverige", list_url="https://www.thenorthface.com/sv-se/c/outlet",
                        observed_at=OBS))
    for t, p, u, im, cat in IKEA_LAST_CHANCE:
        out.append(dict(source="ikea_se", retailer="IKEA", country="SE", currency="SEK", title=t, brand="IKEA",
                        price=p, regular_price=None, category=cat, condition="last_chance",
                        condition_text="Utgår inom kort. / Last chance, being discontinued.",
                        url=IKEA_P + u + "/", url_kind="product", image_url=IKEA_I + im + "?f=s",
                        availability_text="Online och i varuhus", list_url="https://www.ikea.com/se/sv/cat/last-chance/",
                        observed_at="2026-11-15T18:45:00+01:00"))
    return out


if __name__ == "__main__":
    p = pathlib.Path(__file__).with_suffix(".json")
    d = build()
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(d)} records to {p.name}")
