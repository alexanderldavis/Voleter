import os
import sys
import time
import rumps
import numpy
import cv2
import threading

TOGGLE_OSASCRIPT = """osascript -e '
using terms from application "{}"
	if player state of application "{}" is paused then
		tell application "{}" to play
	else
		tell application "{}" to pause
	end if
end using terms from'"""

XMLDOCFIST = """<?xml version="1.0"?>
<opencv_storage>
<cascade>
  <stageType>BOOST</stageType>
  <featureType>HAAR</featureType>
  <height>20</height>
  <width>20</width>
  <stageParams>
    <boostType>GAB</boostType>
    <minHitRate>9.9500000476837158e-01</minHitRate>
    <maxFalseAlarm>5.0000000000000000e-01</maxFalseAlarm>
    <weightTrimRate>9.4999999999999996e-01</weightTrimRate>
    <maxDepth>1</maxDepth>
    <maxWeakCount>1000</maxWeakCount></stageParams>
  <featureParams>
    <maxCatCount>0</maxCatCount>
    <featSize>1</featSize>
    <mode>ALL</mode></featureParams>
  <stageNum>15</stageNum>
  <stages>
    <!-- stage 0 -->
    <_>
      <maxWeakCount>8</maxWeakCount>
      <stageThreshold>-2.2713143825531006e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 201 -5.4666887968778610e-02</internalNodes>
          <leafValues>
            3.3665215969085693e-01 -8.6341208219528198e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 103 3.7254758179187775e-02</internalNodes>
          <leafValues>
            -5.3209882974624634e-01 6.1082488298416138e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 163 -2.7115471661090851e-02</internalNodes>
          <leafValues>
            3.6570644378662109e-01 -5.2932423353195190e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 440 3.3829349558800459e-03</internalNodes>
          <leafValues>
            -2.1344281733036041e-01 6.4416891336441040e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 443 -7.7580874785780907e-03</internalNodes>
          <leafValues>
            6.2000399827957153e-01 -2.0221783220767975e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 113 9.0689714998006821e-03</internalNodes>
          <leafValues>
            -2.8742903470993042e-01 4.2825952172279358e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 195 -2.5702891871333122e-03</internalNodes>
          <leafValues>
            5.7311546802520752e-01 -2.2251150012016296e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 332 -1.4764600200578570e-03</internalNodes>
          <leafValues>
            4.6462264657020569e-01 -2.1650509536266327e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 1 -->
    <_>
      <maxWeakCount>11</maxWeakCount>
      <stageThreshold>-1.9864901304244995e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 202 -1.0966220498085022e-01</internalNodes>
          <leafValues>
            3.2523849606513977e-01 -7.9499757289886475e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 154 2.4816997349262238e-02</internalNodes>
          <leafValues>
            -4.3680062890052795e-01 5.5773758888244629e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 223 1.6977971419692039e-02</internalNodes>
          <leafValues>
            -4.6806603670120239e-01 3.7621638178825378e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 248 -3.6521647125482559e-03</internalNodes>
          <leafValues>
            2.0553478598594666e-01 -5.8883756399154663e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 188 2.2226337343454361e-02</internalNodes>
          <leafValues>
            -1.1979901790618896e-01 7.3377788066864014e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 419 -2.5751888751983643e-02</internalNodes>
          <leafValues>
            6.2296885251998901e-01 -1.9611129164695740e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 437 1.2535196729004383e-03</internalNodes>
          <leafValues>
            -1.7733404040336609e-01 5.9395879507064819e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 82 3.2089389860630035e-02</internalNodes>
          <leafValues>
            -2.2500090301036835e-01 4.6984633803367615e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 424 -2.6619333773851395e-02</internalNodes>
          <leafValues>
            6.8409496545791626e-01 -1.2209472805261612e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 441 1.1945739388465881e-02</internalNodes>
          <leafValues>
            -1.4627437293529510e-01 5.4404318332672119e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 194 -4.7675188630819321e-02</internalNodes>
          <leafValues>
            4.3524911999702454e-01 -1.7861546576023102e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 2 -->
    <_>
      <maxWeakCount>16</maxWeakCount>
      <stageThreshold>-1.9440943002700806e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 173 1.1640264838933945e-01</internalNodes>
          <leafValues>
            -8.1481975317001343e-01 -1.5167931094765663e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 192 5.8329477906227112e-03</internalNodes>
          <leafValues>
            -4.4867351651191711e-01 4.4332587718963623e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 332 -1.4818008057773113e-03</internalNodes>
          <leafValues>
            4.6030735969543457e-01 -2.7868217229843140e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 89 -2.2523095831274986e-03</internalNodes>
          <leafValues>
            2.2774955630302429e-01 -4.8706126213073730e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 196 -2.4854762014001608e-03</internalNodes>
          <leafValues>
            5.4126763343811035e-01 -1.7864058911800385e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 23 4.3165711686015129e-03</internalNodes>
          <leafValues>
            -1.5643970668315887e-01 5.0452882051467896e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 357 1.8938553985208273e-03</internalNodes>
          <leafValues>
            -1.4470857381820679e-01 5.4240542650222778e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 400 1.7599236220121384e-02</internalNodes>
          <leafValues>
            -9.8540179431438446e-02 6.3690596818923950e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 399 -7.4247736483812332e-03</internalNodes>
          <leafValues>
            5.2017074823379517e-01 -1.4347170293331146e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 375 1.7693681642413139e-02</internalNodes>
          <leafValues>
            -1.4774900674819946e-01 5.0748866796493530e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 423 1.1794313788414001e-02</internalNodes>
          <leafValues>
            -1.7001383006572723e-01 5.1170241832733154e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 446 1.6264239326119423e-02</internalNodes>
          <leafValues>
            -9.8087996244430542e-02 6.8675011396408081e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 385 -1.3750856742262840e-02</internalNodes>
          <leafValues>
            3.9213961362838745e-01 -1.7985908687114716e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 109 1.3549974188208580e-02</internalNodes>
          <leafValues>
            -1.5194611251354218e-01 4.9128633737564087e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 9 -2.1129342913627625e-01</internalNodes>
          <leafValues>
            4.2207869887351990e-01 -2.2583450376987457e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 449 1.2446334585547447e-02</internalNodes>
          <leafValues>
            -1.0777114331722260e-01 5.6958603858947754e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 3 -->
    <_>
      <maxWeakCount>22</maxWeakCount>
      <stageThreshold>-2.0477581024169922e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 115 6.9959357380867004e-02</internalNodes>
          <leafValues>
            -8.2081007957458496e-01 -1.6106805205345154e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 156 8.3609884604811668e-03</internalNodes>
          <leafValues>
            -4.1868758201599121e-01 2.9412612318992615e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 353 -7.3514962568879128e-03</internalNodes>
          <leafValues>
            2.7320668101310730e-01 -4.2487537860870361e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 415 -2.7288027107715607e-02</internalNodes>
          <leafValues>
            4.3851810693740845e-01 -1.6587607562541962e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 375 1.4340367168188095e-02</internalNodes>
          <leafValues>
            -1.7406831681728363e-01 4.4700807332992554e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 2 -9.6809107344597578e-04</internalNodes>
          <leafValues>
            -5.4601204395294189e-01 1.3095279037952423e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 262 -1.7094828654080629e-03</internalNodes>
          <leafValues>
            2.4747878313064575e-01 -2.9517665505409241e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 131 2.1775212138891220e-02</internalNodes>
          <leafValues>
            -1.3446959853172302e-01 4.9235558509826660e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 188 2.4628702551126480e-02</internalNodes>
          <leafValues>
            -1.2597034871578217e-01 6.1023765802383423e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 410 -3.3590063452720642e-02</internalNodes>
          <leafValues>
            4.7359499335289001e-01 -1.2634912133216858e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 405 -4.7439346089959145e-03</internalNodes>
          <leafValues>
            4.2270514369010925e-01 -1.3907170295715332e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 439 5.5222143419086933e-03</internalNodes>
          <leafValues>
            -1.4875625073909760e-01 4.0599760413169861e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 311 -1.9990477085229941e-05</internalNodes>
          <leafValues>
            1.8070037662982941e-01 -3.3993247151374817e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 160 -5.6037068367004395e-02</internalNodes>
          <leafValues>
            3.4077924489974976e-01 -1.6916282474994659e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 317 -3.4742974676191807e-03</internalNodes>
          <leafValues>
            4.6804013848304749e-01 -1.4161168038845062e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 28 4.5909948647022247e-02</internalNodes>
          <leafValues>
            -1.0656996816396713e-01 5.4318773746490479e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 453 -5.6191690964624286e-04</internalNodes>
          <leafValues>
            -3.8690611720085144e-01 1.4758817851543427e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 451 2.4836571537889540e-04</internalNodes>
          <leafValues>
            1.5535806119441986e-01 -3.9441427588462830e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 283 -4.4743500649929047e-02</internalNodes>
          <leafValues>
            -7.6658612489700317e-01 6.5931178629398346e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 428 -1.9037872552871704e-02</internalNodes>
          <leafValues>
            3.9858379960060120e-01 -1.5781000256538391e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 443 1.1784614995121956e-02</internalNodes>
          <leafValues>
            -1.2026140838861465e-01 5.2000254392623901e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 337 3.5252270754426718e-03</internalNodes>
          <leafValues>
            -1.4306651055812836e-01 3.7107920646667480e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 4 -->
    <_>
      <maxWeakCount>15</maxWeakCount>
      <stageThreshold>-1.9547632932662964e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 221 1.4877939224243164e-01</internalNodes>
          <leafValues>
            -7.3932796716690063e-01 7.8224100172519684e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 77 -2.0846847444772720e-02</internalNodes>
          <leafValues>
            1.0916696488857269e-01 -5.7142537832260132e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 99 -5.0850339233875275e-02</internalNodes>
          <leafValues>
            5.8871406316757202e-01 -2.1266202628612518e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 276 -1.2801991542801261e-03</internalNodes>
          <leafValues>
            -6.1456012725830078e-01 1.4930143952369690e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 478 -7.3560839518904686e-04</internalNodes>
          <leafValues>
            -5.7494479417800903e-01 1.4662973582744598e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 227 5.0422931963112205e-05</internalNodes>
          <leafValues>
            -3.5570198297500610e-01 2.1197046339511871e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 470 5.6349649094045162e-04</internalNodes>
          <leafValues>
            1.4319466054439545e-01 -5.4962867498397827e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 470 -5.6749995565041900e-04</internalNodes>
          <leafValues>
            -5.7914292812347412e-01 1.7841173708438873e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 478 6.4711406594142318e-04</internalNodes>
          <leafValues>
            1.0261141508817673e-01 -5.2287971973419189e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 274 1.4333154540508986e-03</internalNodes>
          <leafValues>
            1.0357607901096344e-01 -5.7499343156814575e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 413 -4.6389959752559662e-02</internalNodes>
          <leafValues>
            5.5036002397537231e-01 -1.2394639849662781e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 418 2.5023955851793289e-02</internalNodes>
          <leafValues>
            -1.3640131056308746e-01 5.6253921985626221e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 186 -2.0313857021392323e-05</internalNodes>
          <leafValues>
            1.9653269648551941e-01 -3.2664400339126587e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 265 5.5130310356616974e-02</internalNodes>
          <leafValues>
            -9.0591512620449066e-02 6.7299914360046387e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 25 -1.2916579842567444e-02</internalNodes>
          <leafValues>
            5.8651095628738403e-01 -8.0699913203716278e-02</leafValues></_></weakClassifiers></_>
    <!-- stage 5 -->
    <_>
      <maxWeakCount>21</maxWeakCount>
      <stageThreshold>-1.8847852945327759e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 141 1.0149516165256500e-01</internalNodes>
          <leafValues>
            -7.8600162267684937e-01 -1.3344138860702515e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 303 3.9802362152840942e-05</internalNodes>
          <leafValues>
            -5.9213680028915405e-01 3.1743675470352173e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 18 4.3162912130355835e-02</internalNodes>
          <leafValues>
            -2.1775844693183899e-01 4.0945270657539368e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 278 -1.6105859540402889e-03</internalNodes>
          <leafValues>
            -8.2627946138381958e-01 9.3009956181049347e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 273 5.0049996934831142e-03</internalNodes>
          <leafValues>
            9.7198419272899628e-02 -6.8233960866928101e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 162 -1.0944116860628128e-02</internalNodes>
          <leafValues>
            1.1875698715448380e-01 -4.7813010215759277e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 239 3.8121119141578674e-02</internalNodes>
          <leafValues>
            -1.4481469988822937e-01 3.9515179395675659e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 108 -1.1960010975599289e-02</internalNodes>
          <leafValues>
            4.9774870276451111e-01 -1.2315405160188675e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 1 3.3188980887643993e-04</internalNodes>
          <leafValues>
            1.1931858211755753e-01 -4.6453803777694702e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 1 -5.2173522999510169e-04</internalNodes>
          <leafValues>
            -5.9030562639236450e-01 1.1794963479042053e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 421 -1.4819447882473469e-02</internalNodes>
          <leafValues>
            3.1633767485618591e-01 -1.9035957753658295e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 392 6.9389544427394867e-02</internalNodes>
          <leafValues>
            -1.3013434410095215e-01 4.4171881675720215e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 226 1.1210653465241194e-03</internalNodes>
          <leafValues>
            -2.3851880431175232e-01 2.3202013969421387e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 275 4.5368455175776035e-05</internalNodes>
          <leafValues>
            -3.0154618620872498e-01 1.7150510847568512e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 180 -3.8198195397853851e-02</internalNodes>
          <leafValues>
            3.7007099390029907e-01 -1.1945496499538422e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 258 7.1379154920578003e-02</internalNodes>
          <leafValues>
            -8.4876559674739838e-02 5.9651142358779907e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 452 5.9734249953180552e-04</internalNodes>
          <leafValues>
            9.8733007907867432e-02 -5.1181232929229736e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 452 -3.6314019234851003e-04</internalNodes>
          <leafValues>
            -4.3297559022903442e-01 9.9667958915233612e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 146 4.1270256042480469e-03</internalNodes>
          <leafValues>
            5.3097520023584366e-02 -6.8241703510284424e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 64 1.6914984211325645e-02</internalNodes>
          <leafValues>
            -1.3395476341247559e-01 3.3370921015739441e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 36 8.0667492002248764e-03</internalNodes>
          <leafValues>
            5.1350332796573639e-02 -8.8012599945068359e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 6 -->
    <_>
      <maxWeakCount>30</maxWeakCount>
      <stageThreshold>-1.8275513648986816e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 383 7.4466019868850708e-02</internalNodes>
          <leafValues>
            -7.3374384641647339e-01 -1.2699747085571289e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 170 4.5028313994407654e-02</internalNodes>
          <leafValues>
            -3.8118058443069458e-01 2.0441558957099915e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 346 -4.8655350838089362e-05</internalNodes>
          <leafValues>
            1.5811018645763397e-01 -3.7598586082458496e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 12 8.8367000222206116e-02</internalNodes>
          <leafValues>
            -1.6122423112392426e-01 3.3987346291542053e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 19 -4.9912314862012863e-02</internalNodes>
          <leafValues>
            5.7020837068557739e-01 -9.4334475696086884e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 86 -1.5368288382887840e-02</internalNodes>
          <leafValues>
            2.1652756631374359e-01 -2.7887812256813049e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 339 9.9588112789206207e-05</internalNodes>
          <leafValues>
            -3.3919763565063477e-01 1.1196377128362656e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 309 1.8382156267762184e-03</internalNodes>
          <leafValues>
            8.6652971804141998e-02 -7.1336686611175537e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 335 1.2319867964833975e-03</internalNodes>
          <leafValues>
            -1.3563285768032074e-01 3.2173815369606018e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 447 1.5509747900068760e-02</internalNodes>
          <leafValues>
            -8.4733784198760986e-02 4.7326055169105530e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 125 1.5591405332088470e-02</internalNodes>
          <leafValues>
            -1.0504677146673203e-01 3.7859156727790833e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 126 -1.4302727766335011e-02</internalNodes>
          <leafValues>
            4.2119008302688599e-01 -9.2779368162155151e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 313 -1.0954814497381449e-03</internalNodes>
          <leafValues>
            -6.3030725717544556e-01 6.5940104424953461e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 279 -2.1911384537816048e-03</internalNodes>
          <leafValues>
            2.5882127881050110e-01 -1.7156770825386047e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 391 6.4310312271118164e-02</internalNodes>
          <leafValues>
            -1.1839982867240906e-01 3.6049777269363403e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 417 -1.4806499704718590e-02</internalNodes>
          <leafValues>
            3.4870201349258423e-01 -1.4678227901458740e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 467 -4.1603855788707733e-04</internalNodes>
          <leafValues>
            -3.7436413764953613e-01 1.0856705158948898e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 331 -6.2613387126475573e-04</internalNodes>
          <leafValues>
            1.3636322319507599e-01 -2.7424830198287964e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 207 9.6268560737371445e-03</internalNodes>
          <leafValues>
            4.6186465770006180e-02 -7.4375170469284058e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 150 1.3187341392040253e-03</internalNodes>
          <leafValues>
            5.5883128196001053e-02 -5.2970206737518311e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 315 -3.6138594150543213e-02</internalNodes>
          <leafValues>
            -8.1663149595260620e-01 3.6100581288337708e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 304 3.2632466172799468e-04</internalNodes>
          <leafValues>
            -2.6018509268760681e-01 1.2907150387763977e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 442 -3.8270287215709686e-02</internalNodes>
          <leafValues>
            -7.8168857097625732e-01 4.3153896927833557e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 218 2.5224875658750534e-02</internalNodes>
          <leafValues>
            -8.1659168004989624e-02 4.9434235692024231e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 213 -1.7530094832181931e-02</internalNodes>
          <leafValues>
            3.1186184287071228e-01 -1.1343390494585037e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 51 2.2240919992327690e-02</internalNodes>
          <leafValues>
            -8.3505585789680481e-02 4.3163651227951050e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 397 -6.8419501185417175e-03</internalNodes>
          <leafValues>
            2.8975310921669006e-01 -1.2642382085323334e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 10 5.2333518862724304e-02</internalNodes>
          <leafValues>
            -1.4143741130828857e-01 2.7752110362052917e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 189 3.5521041601896286e-02</internalNodes>
          <leafValues>
            -1.7757961153984070e-01 2.9615584015846252e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 406 2.0139083266258240e-02</internalNodes>
          <leafValues>
            -1.0230851173400879e-01 3.7067553400993347e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 7 -->
    <_>
      <maxWeakCount>42</maxWeakCount>
      <stageThreshold>-1.8443435430526733e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 296 8.8901601731777191e-02</internalNodes>
          <leafValues>
            -7.1933221817016602e-01 -1.5627996623516083e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 98 -1.1026700027287006e-02</internalNodes>
          <leafValues>
            4.3406795710325241e-02 -4.1987568140029907e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 27 1.1586422100663185e-02</internalNodes>
          <leafValues>
            -1.2666946649551392e-01 3.6124914884567261e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 249 -3.6935374140739441e-02</internalNodes>
          <leafValues>
            1.3892285525798798e-01 -3.1080135703086853e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 217 -9.3624338507652283e-02</internalNodes>
          <leafValues>
            -4.9779611825942993e-01 1.3059169054031372e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 16 -1.4843516983091831e-02</internalNodes>
          <leafValues>
            5.3876292705535889e-01 -1.1013040691614151e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 190 7.5654466636478901e-03</internalNodes>
          <leafValues>
            -1.2437944859266281e-01 3.3316314220428467e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 153 1.6171240713447332e-03</internalNodes>
          <leafValues>
            9.5025621354579926e-02 -6.2460541725158691e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 281 1.1310473084449768e-02</internalNodes>
          <leafValues>
            -1.8618822097778320e-01 1.9308815896511078e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 461 -1.2596439570188522e-02</internalNodes>
          <leafValues>
            4.1126695275306702e-01 -5.7148765772581100e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 298 -3.2384893856942654e-03</internalNodes>
          <leafValues>
            2.0506007969379425e-01 -1.6527140140533447e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 430 -3.7878248840570450e-02</internalNodes>
          <leafValues>
            4.2533111572265625e-01 -8.4578298032283783e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 242 -1.5176177024841309e-01</internalNodes>
          <leafValues>
            2.7639904618263245e-01 -1.2106479704380035e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 155 -5.8715376071631908e-03</internalNodes>
          <leafValues>
            3.8147667050361633e-01 -1.0069026052951813e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 454 -4.4571753824129701e-04</internalNodes>
          <leafValues>
            -2.4370139837265015e-01 1.1825770884752274e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 229 3.2802019268274307e-04</internalNodes>
          <leafValues>
            -2.7832630276679993e-01 9.9334463477134705e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 122 -9.4857793301343918e-03</internalNodes>
          <leafValues>
            2.5183084607124329e-01 -1.1384104937314987e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 310 3.1689417082816362e-03</internalNodes>
          <leafValues>
            3.6475982517004013e-02 -7.4387818574905396e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 334 -9.2071676626801491e-03</internalNodes>
          <leafValues>
            2.8599455952644348e-01 -1.0032059252262115e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 30 -6.7484982311725616e-02</internalNodes>
          <leafValues>
            -7.6018983125686646e-01 4.1460573673248291e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 261 5.3887993097305298e-02</internalNodes>
          <leafValues>
            -6.9705002009868622e-02 4.3615385890007019e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 246 -1.8193583935499191e-02</internalNodes>
          <leafValues>
            -8.0107253789901733e-01 4.2756892740726471e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 349 2.5610327720642090e-03</internalNodes>
          <leafValues>
            -1.0102678090333939e-01 2.8666132688522339e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 350 -7.5217924313619733e-04</internalNodes>
          <leafValues>
            2.5395667552947998e-01 -1.0963415354490280e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 284 1.9559646025300026e-03</internalNodes>
          <leafValues>
            5.5888641625642776e-02 -5.0882339477539062e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 168 1.7453982727602124e-03</internalNodes>
          <leafValues>
            -1.3242278993129730e-01 2.1177376806735992e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 256 -1.0886035859584808e-02</internalNodes>
          <leafValues>
            2.0701092481613159e-01 -1.6666245460510254e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 142 3.2319794408977032e-03</internalNodes>
          <leafValues>
            5.3879443556070328e-02 -5.4227072000503540e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 361 1.3884394429624081e-03</internalNodes>
          <leafValues>
            4.1983421891927719e-02 -5.5188280344009399e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 176 4.9301609396934509e-02</internalNodes>
          <leafValues>
            -9.4295971095561981e-02 2.9263162612915039e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 352 -1.6199712455272675e-01</internalNodes>
          <leafValues>
            -5.3431183099746704e-01 5.7067964226007462e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 14 -1.4648060314357281e-03</internalNodes>
          <leafValues>
            2.0279650390148163e-01 -1.3912606239318848e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 74 2.8384663164615631e-03</internalNodes>
          <leafValues>
            -9.6340544521808624e-02 2.9700493812561035e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 105 4.8324145376682281e-02</internalNodes>
          <leafValues>
            -1.2372464686632156e-01 2.2127914428710938e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 85 -4.4603561982512474e-03</internalNodes>
          <leafValues>
            3.0666840076446533e-01 -9.7035594284534454e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 184 2.7552039828151464e-03</internalNodes>
          <leafValues>
            4.1796848177909851e-02 -6.9197660684585571e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 468 -4.4074346078559756e-04</internalNodes>
          <leafValues>
            -3.6711362004280090e-01 6.8184144794940948e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 468 5.2346457960084081e-04</internalNodes>
          <leafValues>
            6.7283265292644501e-02 -4.5482447743415833e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 26 1.3168754056096077e-02</internalNodes>
          <leafValues>
            3.3065479248762131e-02 -7.1116536855697632e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 63 8.0091366544365883e-03</internalNodes>
          <leafValues>
            2.4887245148420334e-02 -7.7364140748977661e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 166 7.0955725386738777e-03</internalNodes>
          <leafValues>
            -1.0549836605787277e-01 2.5185430049896240e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 454 3.7571624852716923e-04</internalNodes>
          <leafValues>
            1.0727792978286743e-01 -2.4900336563587189e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 8 -->
    <_>
      <maxWeakCount>43</maxWeakCount>
      <stageThreshold>-1.7893035411834717e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 299 3.5648386925458908e-02</internalNodes>
          <leafValues>
            -7.0296114683151245e-01 -1.2698412872850895e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 270 2.2429595701396465e-03</internalNodes>
          <leafValues>
            -4.1071215271949768e-01 3.5859052091836929e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 17 2.4327874183654785e-02</internalNodes>
          <leafValues>
            -1.5623846650123596e-01 2.9436886310577393e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 75 -1.3620276004076004e-02</internalNodes>
          <leafValues>
            1.1681427061557770e-01 -3.5116511583328247e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 136 8.5835337638854980e-02</internalNodes>
          <leafValues>
            7.9764917492866516e-02 -5.6496101617813110e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 123 4.7699839342385530e-05</internalNodes>
          <leafValues>
            -2.9317864775657654e-01 1.3036113977432251e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 73 -1.0313584655523300e-01</internalNodes>
          <leafValues>
            -6.3222551345825195e-01 5.2599944174289703e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 336 3.4620794467628002e-03</internalNodes>
          <leafValues>
            -1.1524558067321777e-01 2.6946559548377991e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 329 2.5319466367363930e-03</internalNodes>
          <leafValues>
            -9.9124833941459656e-02 2.8651782870292664e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 191 3.5046474076807499e-03</internalNodes>
          <leafValues>
            -1.2839823961257935e-01 2.2405581176280975e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 233 -1.8921627197414637e-03</internalNodes>
          <leafValues>
            3.4105163812637329e-01 -1.1519347876310349e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 88 -1.1282089399173856e-03</internalNodes>
          <leafValues>
            1.0597084462642670e-01 -3.0713862180709839e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 341 -4.5639311429113150e-04</internalNodes>
          <leafValues>
            -3.9502361416816711e-01 7.6203867793083191e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 5 -4.2867049342021346e-04</internalNodes>
          <leafValues>
            -2.7745139598846436e-01 9.8387025296688080e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 6 4.1710381628945470e-04</internalNodes>
          <leafValues>
            1.5602095425128937e-01 -2.6170903444290161e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 462 -5.4169725626707077e-03</internalNodes>
          <leafValues>
            2.5681445002555847e-01 -1.1489927768707275e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 460 8.8902572169899940e-03</internalNodes>
          <leafValues>
            -9.7543835639953613e-02 3.8977515697479248e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 237 9.2598721385002136e-03</internalNodes>
          <leafValues>
            -1.0659169405698776e-01 2.6013055443763733e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 197 -2.5082924403250217e-03</internalNodes>
          <leafValues>
            2.6170146465301514e-01 -1.1003012210130692e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 181 -1.0551470331847668e-02</internalNodes>
          <leafValues>
            2.0596505701541901e-01 -1.4270199835300446e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 49 -1.8921995069831610e-03</internalNodes>
          <leafValues>
            -2.8097373247146606e-01 9.5069833099842072e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 47 3.4997303737327456e-04</internalNodes>
          <leafValues>
            7.4786894023418427e-02 -3.2906740903854370e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 182 -2.9982118867337704e-03</internalNodes>
          <leafValues>
            -6.4655232429504395e-01 3.3920895308256149e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 253 1.5988170634955168e-03</internalNodes>
          <leafValues>
            -9.6316106617450714e-02 2.5733822584152222e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 253 -1.0750601068139076e-03</internalNodes>
          <leafValues>
            2.3550213873386383e-01 -9.9042907357215881e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 382 -1.1690751463174820e-01</internalNodes>
          <leafValues>
            -4.1904076933860779e-01 5.8113947510719299e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 272 -5.7531986385583878e-04</internalNodes>
          <leafValues>
            -4.3666678667068481e-01 5.4361913353204727e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 356 -1.4746581437066197e-03</internalNodes>
          <leafValues>
            2.6427274942398071e-01 -9.3144074082374573e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 411 2.0219152793288231e-03</internalNodes>
          <leafValues>
            -1.0835584253072739e-01 2.1407759189605713e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 40 2.4618413299322128e-02</internalNodes>
          <leafValues>
            -5.4161112755537033e-02 4.3121159076690674e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 443 -8.1046596169471741e-03</internalNodes>
          <leafValues>
            2.3591291904449463e-01 -9.9035874009132385e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 446 7.0481696166098118e-03</internalNodes>
          <leafValues>
            -1.0464326292276382e-01 2.5947844982147217e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 269 -6.6838287748396397e-03</internalNodes>
          <leafValues>
            5.2856040000915527e-01 -4.5856099575757980e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 297 1.1845057830214500e-02</internalNodes>
          <leafValues>
            3.8581307977437973e-02 -7.7163338661193848e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 90 -1.5032331459224224e-02</internalNodes>
          <leafValues>
            1.2219436466693878e-01 -2.0751366019248962e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 35 -4.3774796649813652e-03</internalNodes>
          <leafValues>
            -7.4121695756912231e-01 3.0329445376992226e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 165 2.9580652713775635e-02</internalNodes>
          <leafValues>
            3.0603853985667229e-02 -6.0506159067153931e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 254 2.0463918335735798e-03</internalNodes>
          <leafValues>
            -9.5472671091556549e-02 2.5378978252410889e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 286 9.6978545188903809e-03</internalNodes>
          <leafValues>
            3.4235402941703796e-02 -7.0167511701583862e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 328 6.9205567706376314e-04</internalNodes>
          <leafValues>
            -1.0737954080104828e-01 2.2037743031978607e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 377 -6.8107126280665398e-03</internalNodes>
          <leafValues>
            2.1109257638454437e-01 -1.0865246504545212e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 474 -2.0692136138677597e-02</internalNodes>
          <leafValues>
            -4.2843049764633179e-01 6.2190957367420197e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 363 -9.8479548469185829e-03</internalNodes>
          <leafValues>
            -5.4518640041351318e-01 3.8433585315942764e-02</leafValues></_></weakClassifiers></_>
    <!-- stage 9 -->
    <_>
      <maxWeakCount>44</maxWeakCount>
      <stageThreshold>-1.7278813123703003e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 143 5.5534072220325470e-02</internalNodes>
          <leafValues>
            -7.2150355577468872e-01 -1.7668160796165466e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 29 8.4920674562454224e-03</internalNodes>
          <leafValues>
            -2.8496882319450378e-01 2.2688460350036621e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 351 -4.1526146233081818e-02</internalNodes>
          <leafValues>
            1.6426217555999756e-01 -2.8602874279022217e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 447 -1.5268056653439999e-02</internalNodes>
          <leafValues>
            3.3429688215255737e-01 -1.0207356512546539e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 1 3.3309031277894974e-04</internalNodes>
          <leafValues>
            8.8365651667118073e-02 -3.7201511859893799e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 1 -2.0692260295618325e-04</internalNodes>
          <leafValues>
            -2.8830185532569885e-01 1.5212041139602661e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 91 -8.8329076766967773e-02</internalNodes>
          <leafValues>
            -7.3895603418350220e-01 3.7705518305301666e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 199 8.9851923286914825e-02</internalNodes>
          <leafValues>
            7.3726423084735870e-02 -3.7346929311752319e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 271 5.2115610742475837e-05</internalNodes>
          <leafValues>
            -2.7822205424308777e-01 1.0110668838024139e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 228 4.6711592003703117e-03</internalNodes>
          <leafValues>
            6.3592813909053802e-02 -5.8029443025588989e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 403 1.8238683696836233e-03</internalNodes>
          <leafValues>
            -1.1548501253128052e-01 2.6030620932579041e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 33 -1.7950371839106083e-03</internalNodes>
          <leafValues>
            2.2334524989128113e-01 -1.1683943867683411e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 116 6.2029501423239708e-03</internalNodes>
          <leafValues>
            4.9092683941125870e-02 -5.9445142745971680e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 443 1.4308722689747810e-02</internalNodes>
          <leafValues>
            -8.2489550113677979e-02 3.2171344757080078e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 312 -1.8367242300882936e-03</internalNodes>
          <leafValues>
            -8.1535130739212036e-01 3.2583583146333694e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 41 1.9530367106199265e-02</internalNodes>
          <leafValues>
            -8.0674402415752411e-02 3.3977818489074707e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 302 7.5637712143361568e-04</internalNodes>
          <leafValues>
            -1.7070209980010986e-01 1.5529455244541168e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 267 -1.3595197349786758e-02</internalNodes>
          <leafValues>
            5.5791413784027100e-01 -5.5808130651712418e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 159 4.3131947517395020e-02</internalNodes>
          <leafValues>
            4.1752044111490250e-02 -6.5074503421783447e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 255 5.4025306599214673e-04</internalNodes>
          <leafValues>
            -1.3719789683818817e-01 1.9081442058086395e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 220 1.8056023120880127e-01</internalNodes>
          <leafValues>
            -4.5487821102142334e-02 5.7150274515151978e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 46 8.5341639351099730e-04</internalNodes>
          <leafValues>
            9.5420971512794495e-02 -2.7156314253807068e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 234 2.8430842794477940e-03</internalNodes>
          <leafValues>
            -1.3535773754119873e-01 1.8309751152992249e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 157 -9.4798579812049866e-03</internalNodes>
          <leafValues>
            3.7719145417213440e-01 -8.3122611045837402e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 318 2.1699026226997375e-02</internalNodes>
          <leafValues>
            -1.2101063877344131e-01 2.1229124069213867e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 340 3.8566322473343462e-05</internalNodes>
          <leafValues>
            -2.2390285134315491e-01 1.1792477965354919e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 54 -1.8031906336545944e-02</internalNodes>
          <leafValues>
            -4.4144934415817261e-01 5.9715121984481812e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 435 6.6676503047347069e-04</internalNodes>
          <leafValues>
            -1.0740659385919571e-01 2.4743415415287018e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 365 1.9775887485593557e-03</internalNodes>
          <leafValues>
            -9.4217516481876373e-02 2.5528213381767273e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 45 1.1575685441493988e-01</internalNodes>
          <leafValues>
            -5.2362650632858276e-02 4.6459662914276123e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 306 -7.2900601662695408e-04</internalNodes>
          <leafValues>
            -4.7743988037109375e-01 5.5707260966300964e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 477 -8.6085777729749680e-03</internalNodes>
          <leafValues>
            -3.4801360964775085e-01 6.7196793854236603e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 450 9.8475767299532890e-03</internalNodes>
          <leafValues>
            -8.2833766937255859e-02 2.9720556735992432e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 372 -5.0170894246548414e-04</internalNodes>
          <leafValues>
            1.7210811376571655e-01 -1.5405090153217316e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 118 -5.9569685254245996e-04</internalNodes>
          <leafValues>
            -4.2103236913681030e-01 5.4986894130706787e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 145 -1.6659650951623917e-02</internalNodes>
          <leafValues>
            4.8574015498161316e-01 -5.3368117660284042e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 188 1.6228452324867249e-02</internalNodes>
          <leafValues>
            -8.1653036177158356e-02 2.9283285140991211e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 15 9.6935760229825974e-03</internalNodes>
          <leafValues>
            -1.0168474912643433e-01 3.0204299092292786e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 48 8.3334033843129873e-04</internalNodes>
          <leafValues>
            5.3272679448127747e-02 -4.7765058279037476e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 112 -5.0984360277652740e-03</internalNodes>
          <leafValues>
            8.6067497730255127e-02 -2.7194350957870483e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 211 2.3798914626240730e-03</internalNodes>
          <leafValues>
            -7.9323202371597290e-02 2.8626143932342529e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 456 6.9782495498657227e-02</internalNodes>
          <leafValues>
            -5.8496922254562378e-02 3.7700223922729492e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 320 5.5434880778193474e-03</internalNodes>
          <leafValues>
            -2.8883689641952515e-01 8.5519842803478241e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 185 1.4064475544728339e-04</internalNodes>
          <leafValues>
            -2.0895852148532867e-01 1.0705342888832092e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 10 -->
    <_>
      <maxWeakCount>49</maxWeakCount>
      <stageThreshold>-1.8219289779663086e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 426 7.6211318373680115e-02</internalNodes>
          <leafValues>
            -7.1837830543518066e-01 -3.3020132780075073e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 379 -2.0481327548623085e-02</internalNodes>
          <leafValues>
            9.5462836325168610e-02 -3.6154863238334656e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 129 -1.8238006159663200e-02</internalNodes>
          <leafValues>
            3.3872231841087341e-01 -1.3804213702678680e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 97 -4.7343150072265416e-05</internalNodes>
          <leafValues>
            1.4024296402931213e-01 -2.4231317639350891e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 188 2.7541581541299820e-02</internalNodes>
          <leafValues>
            -7.6362438499927521e-02 4.6329486370086670e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 472 -9.8395291715860367e-03</internalNodes>
          <leafValues>
            3.6118632555007935e-01 -7.6510980725288391e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 387 1.6506291925907135e-02</internalNodes>
          <leafValues>
            -9.9370971322059631e-02 3.8026013970375061e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 393 1.4908757060766220e-02</internalNodes>
          <leafValues>
            7.2971321642398834e-02 -4.1126790642738342e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 0 -2.7689849957823753e-04</internalNodes>
          <leafValues>
            -3.1757867336273193e-01 1.1926878988742828e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 8 6.8625565618276596e-03</internalNodes>
          <leafValues>
            -1.3300311565399170e-01 2.3616589605808258e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 314 1.7563775181770325e-02</internalNodes>
          <leafValues>
            -1.0701343417167664e-01 2.8075546026229858e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 398 5.4760114289820194e-03</internalNodes>
          <leafValues>
            -1.1317989975214005e-01 3.0863639712333679e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 24 1.8663737922906876e-02</internalNodes>
          <leafValues>
            -7.2062864899635315e-02 4.0031290054321289e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 137 3.1435843557119370e-02</internalNodes>
          <leafValues>
            -8.6014658212661743e-02 3.5046252608299255e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 370 1.5856244135648012e-03</internalNodes>
          <leafValues>
            -1.0674177855253220e-01 2.6674389839172363e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 42 -4.2580462992191315e-02</internalNodes>
          <leafValues>
            4.1299226880073547e-01 -6.8977311253547668e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 416 1.6159350052475929e-03</internalNodes>
          <leafValues>
            -1.2306774407625198e-01 2.3529247939586639e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 290 2.3702822625637054e-02</internalNodes>
          <leafValues>
            3.7473268806934357e-02 -7.3936849832534790e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 389 -5.4993435740470886e-02</internalNodes>
          <leafValues>
            -7.1363353729248047e-01 3.5479776561260223e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 414 -1.4394074678421021e-03</internalNodes>
          <leafValues>
            2.4060715734958649e-01 -1.2430076301097870e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 95 2.5124833919107914e-03</internalNodes>
          <leafValues>
            5.5541750043630600e-02 -5.0494503974914551e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 473 1.8378920853137970e-02</internalNodes>
          <leafValues>
            5.1005601882934570e-02 -5.0084227323532104e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 179 5.3248797485139221e-05</internalNodes>
          <leafValues>
            -2.4983724951744080e-01 1.0383369028568268e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 81 -2.7512156520970166e-04</internalNodes>
          <leafValues>
            -2.6547372341156006e-01 9.6457287669181824e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 0 1.8864774028770626e-04</internalNodes>
          <leafValues>
            1.0292784869670868e-01 -2.5061330199241638e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 140 5.9512788429856300e-03</internalNodes>
          <leafValues>
            -1.1717485636472702e-01 2.4074864387512207e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 164 -4.1379258036613464e-02</internalNodes>
          <leafValues>
            -6.0395568609237671e-01 4.2426131665706635e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 445 -1.9872462376952171e-02</internalNodes>
          <leafValues>
            -5.4396378993988037e-01 4.3562423437833786e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 177 5.9608366427710280e-05</internalNodes>
          <leafValues>
            -2.0209309458732605e-01 1.2704248726367950e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 362 -1.0295662796124816e-03</internalNodes>
          <leafValues>
            2.5254362821578979e-01 -1.0863963514566422e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 147 1.2053424492478371e-02</internalNodes>
          <leafValues>
            -1.3459467887878418e-01 2.0055423676967621e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 31 2.5347635149955750e-01</internalNodes>
          <leafValues>
            5.4883647710084915e-02 -5.7278418540954590e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 104 -3.0894479155540466e-01</internalNodes>
          <leafValues>
            3.5593131184577942e-01 -8.6552262306213379e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 264 5.9521459043025970e-02</internalNodes>
          <leafValues>
            -6.9592170417308807e-02 3.9193993806838989e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 50 2.4012567475438118e-02</internalNodes>
          <leafValues>
            -7.0487909018993378e-02 3.3367377519607544e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 47 -3.7590277497656643e-04</internalNodes>
          <leafValues>
            -2.6074239611625671e-01 9.6643641591072083e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 187 5.2923976909369230e-04</internalNodes>
          <leafValues>
            -1.8706458806991577e-01 1.3947336375713348e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 183 3.6549959331750870e-03</internalNodes>
          <leafValues>
            4.8172671347856522e-02 -5.2832067012786865e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 125 -4.2269211262464523e-03</internalNodes>
          <leafValues>
            2.2982832789421082e-01 -1.1057103425264359e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 241 -1.5791966579854488e-03</internalNodes>
          <leafValues>
            2.4724601209163666e-01 -9.9960461258888245e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 236 3.2143674790859222e-02</internalNodes>
          <leafValues>
            4.1846901178359985e-02 -6.7717236280441284e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 151 -4.5216959551908076e-04</internalNodes>
          <leafValues>
            -3.4453940391540527e-01 6.5845489501953125e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 209 -1.5516865532845259e-03</internalNodes>
          <leafValues>
            3.2929363846778870e-01 -7.9869076609611511e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 210 8.1252021482214332e-04</internalNodes>
          <leafValues>
            -1.1332812160253525e-01 2.8165125846862793e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 376 -2.4522520601749420e-02</internalNodes>
          <leafValues>
            -4.5872429013252258e-01 4.9399010837078094e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 204 1.8506310880184174e-02</internalNodes>
          <leafValues>
            3.2849080860614777e-02 -6.3140118122100830e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 263 -4.2467348277568817e-02</internalNodes>
          <leafValues>
            -7.3348873853683472e-01 2.5894951075315475e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 475 -7.4512483552098274e-03</internalNodes>
          <leafValues>
            2.4213030934333801e-01 -1.1624603718519211e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 381 -8.1274705007672310e-03</internalNodes>
          <leafValues>
            2.1939149498939514e-01 -1.0876557230949402e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 11 -->
    <_>
      <maxWeakCount>46</maxWeakCount>
      <stageThreshold>-1.6810785531997681e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 69 6.2926054000854492e-02</internalNodes>
          <leafValues>
            -7.3015433549880981e-01 -3.9503166079521179e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 78 -2.5521781295537949e-02</internalNodes>
          <leafValues>
            4.2592626065015793e-02 -3.7622928619384766e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 120 -1.4039221405982971e-01</internalNodes>
          <leafValues>
            2.5563183426856995e-01 -1.3284343481063843e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 292 -3.0109984800219536e-03</internalNodes>
          <leafValues>
            1.1356259137392044e-01 -2.8744885325431824e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 11 -3.5497295903041959e-04</internalNodes>
          <leafValues>
            -3.0102956295013428e-01 1.3360467553138733e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 11 4.1976163629442453e-04</internalNodes>
          <leafValues>
            1.0632297396659851e-01 -4.1465765237808228e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 57 -6.0904128476977348e-03</internalNodes>
          <leafValues>
            3.2988336682319641e-01 -9.0175963938236237e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 224 3.0226586386561394e-04</internalNodes>
          <leafValues>
            -2.5316438078880310e-01 1.0844703018665314e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 452 -3.2072147587314248e-04</internalNodes>
          <leafValues>
            -3.4653735160827637e-01 9.4577670097351074e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 452 2.7857549139298499e-04</internalNodes>
          <leafValues>
            1.0215818136930466e-01 -3.3458346128463745e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 251 1.0500374436378479e-01</internalNodes>
          <leafValues>
            2.8705380856990814e-02 -7.9022705554962158e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 438 -1.7730401596054435e-03</internalNodes>
          <leafValues>
            2.5074681639671326e-01 -1.0478724539279938e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 438 1.7741168849170208e-03</internalNodes>
          <leafValues>
            -1.4734008908271790e-01 2.9280042648315430e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 252 1.1175869032740593e-02</internalNodes>
          <leafValues>
            3.9055425673723221e-02 -6.5613752603530884e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 106 -1.0290768928825855e-02</internalNodes>
          <leafValues>
            3.4194087982177734e-01 -7.6268434524536133e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 156 4.6540973708033562e-03</internalNodes>
          <leafValues>
            -1.6472984850406647e-01 1.9732075929641724e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 371 1.1035171337425709e-03</internalNodes>
          <leafValues>
            -1.7102368175983429e-01 1.5059606730937958e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 121 -7.6700694626197219e-04</internalNodes>
          <leafValues>
            -4.8405992984771729e-01 5.2564583718776703e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 196 -1.2061977759003639e-03</internalNodes>
          <leafValues>
            2.1690566837787628e-01 -1.0669865459203720e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 135 9.1797057539224625e-03</internalNodes>
          <leafValues>
            4.6832177788019180e-02 -4.7986325621604919e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 289 1.1840627994388342e-03</internalNodes>
          <leafValues>
            -1.1005662381649017e-01 2.5596213340759277e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 203 3.5268035717308521e-03</internalNodes>
          <leafValues>
            -9.0739317238330841e-02 3.3515402674674988e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 235 -4.9964886158704758e-02</internalNodes>
          <leafValues>
            -6.2811344861984253e-01 3.5539835691452026e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 464 -2.5685567408800125e-02</internalNodes>
          <leafValues>
            -6.6798198223114014e-01 2.7661748230457306e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 214 1.3474756479263306e-01</internalNodes>
          <leafValues>
            -5.8762442320585251e-02 4.1361138224601746e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 62 5.1215805113315582e-02</internalNodes>
          <leafValues>
            -9.1004416346549988e-02 2.5584313273429871e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 21 -2.9197093099355698e-03</internalNodes>
          <leafValues>
            2.5383532047271729e-01 -1.0009348392486572e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 465 -2.9864147305488586e-02</internalNodes>
          <leafValues>
            4.8189738392829895e-01 -5.0785746425390244e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 321 -1.1807624995708466e-01</internalNodes>
          <leafValues>
            2.1991235017776489e-01 -1.1988802254199982e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 359 3.8068499416112900e-03</internalNodes>
          <leafValues>
            3.5180743783712387e-02 -6.7576938867568970e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 367 8.6970794945955276e-03</internalNodes>
          <leafValues>
            -1.5224443376064301e-01 1.4459002017974854e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 2 -9.5600984059274197e-04</internalNodes>
          <leafValues>
            -3.7121850252151489e-01 6.2214512377977371e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 158 6.9636516273021698e-02</internalNodes>
          <leafValues>
            2.5314794853329659e-02 -7.4594342708587646e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 374 -9.3403244391083717e-03</internalNodes>
          <leafValues>
            2.6523110270500183e-01 -8.9643396437168121e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 375 1.3769559562206268e-02</internalNodes>
          <leafValues>
            -9.0301707386970520e-02 2.3445534706115723e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 266 3.3872486092150211e-03</internalNodes>
          <leafValues>
            -7.1965888142585754e-02 3.0522763729095459e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 333 -1.7513568745926023e-03</internalNodes>
          <leafValues>
            2.7926686406135559e-01 -1.0522783547639847e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 148 4.8992798838298768e-05</internalNodes>
          <leafValues>
            -1.9681489467620850e-01 1.2212883681058884e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 216 5.7211164385080338e-03</internalNodes>
          <leafValues>
            2.8904886916279793e-02 -7.3670428991317749e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 124 -8.0895749852061272e-03</internalNodes>
          <leafValues>
            2.1025183796882629e-01 -1.0317879170179367e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 358 -1.0087373666465282e-02</internalNodes>
          <leafValues>
            2.2240601480007172e-01 -1.0200151056051254e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 102 -3.6124540492892265e-03</internalNodes>
          <leafValues>
            2.5013539195060730e-01 -8.6151108145713806e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 47 4.3964933138340712e-04</internalNodes>
          <leafValues>
            6.5888963639736176e-02 -3.4074530005455017e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 44 1.7187757417559624e-02</internalNodes>
          <leafValues>
            -7.7297151088714600e-02 3.0144968628883362e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 277 -3.4325954038649797e-04</internalNodes>
          <leafValues>
            1.0410871356725693e-01 -2.3695227503776550e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 65 -3.5277014831081033e-04</internalNodes>
          <leafValues>
            -2.5119048357009888e-01 9.5483288168907166e-02</leafValues></_></weakClassifiers></_>
    <!-- stage 12 -->
    <_>
      <maxWeakCount>65</maxWeakCount>
      <stageThreshold>-1.7414934635162354e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 355 4.1296590119600296e-02</internalNodes>
          <leafValues>
            -7.0528686046600342e-01 -3.5626912117004395e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 22 4.0419185534119606e-03</internalNodes>
          <leafValues>
            -3.0594900250434875e-01 8.4412172436714172e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 380 -1.4193544164299965e-02</internalNodes>
          <leafValues>
            1.0406953841447830e-01 -2.7606400847434998e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 344 -3.2072613248601556e-04</internalNodes>
          <leafValues>
            1.1246731132268906e-01 -2.0575453341007233e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 76 2.7554212138056755e-03</internalNodes>
          <leafValues>
            -8.1184990704059601e-02 2.9940533638000488e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 478 -4.3844751780852675e-04</internalNodes>
          <leafValues>
            -3.0456635355949402e-01 8.9931130409240723e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 188 -2.9951043426990509e-02</internalNodes>
          <leafValues>
            2.9456126689910889e-01 -7.3855355381965637e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 469 6.3217978458851576e-04</internalNodes>
          <leafValues>
            8.1928633153438568e-02 -2.7957710623741150e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 422 2.6375630870461464e-02</internalNodes>
          <leafValues>
            -7.5757406651973724e-02 3.0115717649459839e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 240 -1.6676289960741997e-03</internalNodes>
          <leafValues>
            2.3177707195281982e-01 -9.9907495081424713e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 238 2.3822035640478134e-02</internalNodes>
          <leafValues>
            -1.2906464934349060e-01 1.8870647251605988e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 308 2.8320599813014269e-03</internalNodes>
          <leafValues>
            5.3110528737306595e-02 -4.1562080383300781e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 324 9.2108000535517931e-04</internalNodes>
          <leafValues>
            -9.8274961113929749e-02 2.2691772878170013e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 324 -7.4534956365823746e-04</internalNodes>
          <leafValues>
            2.3881106078624725e-01 -1.0162839293479919e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 327 5.4611634463071823e-02</internalNodes>
          <leafValues>
            3.9110615849494934e-02 -5.8543741703033447e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 396 -4.2007807642221451e-03</internalNodes>
          <leafValues>
            1.8320231139659882e-01 -1.1496944725513458e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 305 -4.7572434414178133e-04</internalNodes>
          <leafValues>
            -3.7265035510063171e-01 5.6087024509906769e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 268 -1.9487980753183365e-02</internalNodes>
          <leafValues>
            5.0985199213027954e-01 -4.2160559445619583e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 332 -1.8599908798933029e-03</internalNodes>
          <leafValues>
            1.7994043231010437e-01 -1.3731285929679871e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 60 -1.1626982130110264e-02</internalNodes>
          <leafValues>
            -5.5860477685928345e-01 4.2699787765741348e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 243 1.6678202897310257e-02</internalNodes>
          <leafValues>
            2.6586018502712250e-02 -7.2350299358367920e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 174 2.8998608468100429e-04</internalNodes>
          <leafValues>
            -1.3143455982208252e-01 1.6071778535842896e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 144 4.9336016672896221e-05</internalNodes>
          <leafValues>
            -2.1794757246971130e-01 1.0093602538108826e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 323 -3.7926372606307268e-03</internalNodes>
          <leafValues>
            -3.2599428296089172e-01 6.7336559295654297e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 330 1.2762554921209812e-02</internalNodes>
          <leafValues>
            -5.5437177419662476e-02 3.8652956485748291e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 434 -6.4559504389762878e-03</internalNodes>
          <leafValues>
            1.9700351357460022e-01 -9.5786385238170624e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 55 -2.2290320694446564e-01</internalNodes>
          <leafValues>
            2.7592590451240540e-01 -9.7534365952014923e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 215 3.7266150116920471e-02</internalNodes>
          <leafValues>
            -4.9471620470285416e-02 5.2692419290542603e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 58 -6.5337857231497765e-03</internalNodes>
          <leafValues>
            -3.2230788469314575e-01 6.4922027289867401e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 366 3.3789561130106449e-03</internalNodes>
          <leafValues>
            -8.1151612102985382e-02 2.5136163830757141e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 200 2.1851856261491776e-02</internalNodes>
          <leafValues>
            4.2013950645923615e-02 -4.7490635514259338e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 402 1.7539365217089653e-03</internalNodes>
          <leafValues>
            -9.5588095486164093e-02 2.2242130339145660e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 288 -6.5333157544955611e-04</internalNodes>
          <leafValues>
            2.2608472406864166e-01 -8.8774204254150391e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 285 3.9327275007963181e-03</internalNodes>
          <leafValues>
            -7.0321895182132721e-02 2.8162205219268799e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 322 -1.8236566334962845e-02</internalNodes>
          <leafValues>
            -5.4569953680038452e-01 3.8036964833736420e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 338 -9.0195581316947937e-02</internalNodes>
          <leafValues>
            -6.4631688594818115e-01 2.4201860651373863e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 259 -3.6988611100241542e-04</internalNodes>
          <leafValues>
            1.1717893928289413e-01 -1.7016832530498505e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 101 -2.0807310938835144e-02</internalNodes>
          <leafValues>
            -3.5712221264839172e-01 5.1320154219865799e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 348 1.2778453528881073e-03</internalNodes>
          <leafValues>
            -8.3930484950542450e-02 2.3301397264003754e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 412 2.7555268257856369e-02</internalNodes>
          <leafValues>
            3.9710119366645813e-02 -4.9064424633979797e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 92 1.9331908551976085e-03</internalNodes>
          <leafValues>
            4.3063085526227951e-02 -4.0544021129608154e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 133 -3.7927129305899143e-03</internalNodes>
          <leafValues>
            -9.7478276491165161e-01 1.5725808218121529e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 149 1.4201332814991474e-03</internalNodes>
          <leafValues>
            -1.8027123808860779e-01 9.4606719911098480e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 128 6.8884089589118958e-02</internalNodes>
          <leafValues>
            -7.0725709199905396e-02 2.6525896787643433e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 53 1.0850091930478811e-03</internalNodes>
          <leafValues>
            8.3277270197868347e-02 -2.3897601664066315e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 7 -1.1585891479626298e-03</internalNodes>
          <leafValues>
            -2.5561347603797913e-01 6.8587794899940491e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 34 -4.3306900188326836e-03</internalNodes>
          <leafValues>
            2.8104227781295776e-01 -6.8212784826755524e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 227 -1.0543361713644117e-04</internalNodes>
          <leafValues>
            -2.5780510902404785e-01 7.1489281952381134e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 294 6.6599401179701090e-04</internalNodes>
          <leafValues>
            -9.3447253108024597e-02 1.9375421106815338e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 93 9.0444379020482302e-04</internalNodes>
          <leafValues>
            4.8062358051538467e-02 -3.8001146912574768e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 39 1.5007372712716460e-03</internalNodes>
          <leafValues>
            -8.4309920668601990e-02 2.4136951565742493e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 291 9.7632735967636108e-02</internalNodes>
          <leafValues>
            -2.5545349344611168e-02 7.2601866722106934e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 388 -5.6443312205374241e-03</internalNodes>
          <leafValues>
            2.1070015430450439e-01 -8.5336968302726746e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 205 6.8177446722984314e-02</internalNodes>
          <leafValues>
            2.1576214581727982e-02 -8.6731415987014771e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 171 1.2811918277293444e-03</internalNodes>
          <leafValues>
            5.6091584265232086e-02 -2.9650855064392090e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 260 2.2776387631893158e-02</internalNodes>
          <leafValues>
            -6.2589645385742188e-02 2.9604688286781311e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 448 8.2068433985114098e-03</internalNodes>
          <leafValues>
            3.4876767545938492e-02 -5.4241234064102173e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 364 -1.7591845244169235e-02</internalNodes>
          <leafValues>
            -4.8125627636909485e-01 3.3481091260910034e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 114 -4.1520636528730392e-02</internalNodes>
          <leafValues>
            4.5658212900161743e-01 -4.8344220966100693e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 247 2.9943633824586868e-02</internalNodes>
          <leafValues>
            -4.3336339294910431e-02 4.3473845720291138e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 161 2.8948470950126648e-02</internalNodes>
          <leafValues>
            6.9669134914875031e-02 -2.7212557196617126e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 71 -1.8850958347320557e-01</internalNodes>
          <leafValues>
            -4.5135584473609924e-01 3.7534955888986588e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 80 1.5133740380406380e-03</internalNodes>
          <leafValues>
            -1.0431765019893646e-01 1.6860207915306091e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 232 -8.1167835742235184e-04</internalNodes>
          <leafValues>
            -4.2089194059371948e-01 4.1012953966856003e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 420 1.0125419124960899e-02</internalNodes>
          <leafValues>
            2.1643577143549919e-02 -7.0689058303833008e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 13 -->
    <_>
      <maxWeakCount>58</maxWeakCount>
      <stageThreshold>-1.7014893293380737e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 130 1.9178355112671852e-02</internalNodes>
          <leafValues>
            -7.1919542551040649e-01 -3.9400666952133179e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 432 -9.6830362454056740e-03</internalNodes>
          <leafValues>
            1.1073518544435501e-01 -2.7416533231735229e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 84 -2.6433897018432617e-01</internalNodes>
          <leafValues>
            2.2881194949150085e-01 -1.3337633013725281e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 454 -4.7765963245183229e-04</internalNodes>
          <leafValues>
            -2.1894542872905731e-01 1.0748665034770966e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 326 -9.5769145991653204e-04</internalNodes>
          <leafValues>
            1.1148676276206970e-01 -2.8165405988693237e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 293 1.7252839170396328e-03</internalNodes>
          <leafValues>
            -7.4313938617706299e-02 3.5713282227516174e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 301 2.5283906143158674e-04</internalNodes>
          <leafValues>
            -1.5409423410892487e-01 1.5306258201599121e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 407 1.1587433516979218e-02</internalNodes>
          <leafValues>
            -3.6668900400400162e-02 3.9697381854057312e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 407 -5.6802378967404366e-03</internalNodes>
          <leafValues>
            1.9254903495311737e-01 -1.2040124833583832e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 193 1.1539794504642487e-02</internalNodes>
          <leafValues>
            -1.0144866257905960e-01 2.4409648776054382e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 188 2.4630051106214523e-02</internalNodes>
          <leafValues>
            -8.1282690167427063e-02 3.2874536514282227e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 56 3.0628627538681030e-01</internalNodes>
          <leafValues>
            -7.3277726769447327e-02 3.2925745844841003e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 433 9.0348850935697556e-03</internalNodes>
          <leafValues>
            -8.7457589805126190e-02 2.7506023645401001e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 79 -5.4765380918979645e-02</internalNodes>
          <leafValues>
            1.8219882249832153e-01 -1.2832860648632050e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 169 -1.0856217704713345e-02</internalNodes>
          <leafValues>
            2.9163876175880432e-01 -8.7499432265758514e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 262 -1.3364129699766636e-03</internalNodes>
          <leafValues>
            9.8299294710159302e-02 -2.3856776952743530e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 345 -8.7236036779358983e-04</internalNodes>
          <leafValues>
            -5.2250921726226807e-01 3.8880791515111923e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 20 -6.4848095178604126e-02</internalNodes>
          <leafValues>
            -7.2697210311889648e-01 2.4495918303728104e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 360 -9.3917513731867075e-04</internalNodes>
          <leafValues>
            1.6033267974853516e-01 -1.1950765550136566e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 471 -1.9280787557363510e-02</internalNodes>
          <leafValues>
            -2.2314575314521790e-01 8.4325037896633148e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 119 2.6243243366479874e-02</internalNodes>
          <leafValues>
            2.8311902657151222e-02 -6.3425910472869873e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 212 2.7750162407755852e-03</internalNodes>
          <leafValues>
            4.2481195181608200e-02 -4.0530085563659668e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 167 1.9279066473245621e-03</internalNodes>
          <leafValues>
            -7.3377959430217743e-02 2.7781105041503906e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 110 2.3176665417850018e-03</internalNodes>
          <leafValues>
            -1.0286873579025269e-01 2.2891710698604584e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 100 -8.1800833344459534e-02</internalNodes>
          <leafValues>
            2.9631137847900391e-01 -7.2752080857753754e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 32 -1.0096825426444411e-03</internalNodes>
          <leafValues>
            1.5619809925556183e-01 -1.3750164210796356e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 37 8.4614939987659454e-03</internalNodes>
          <leafValues>
            2.6721300557255745e-02 -6.9235771894454956e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 233 -2.8171993326395750e-03</internalNodes>
          <leafValues>
            2.5952735543251038e-01 -7.6076589524745941e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 378 2.7538510039448738e-03</internalNodes>
          <leafValues>
            -6.4811497926712036e-02 2.7650922536849976e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 390 -3.2651454675942659e-03</internalNodes>
          <leafValues>
            2.0635053515434265e-01 -1.2169247865676880e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 431 -6.0873263282701373e-04</internalNodes>
          <leafValues>
            -3.0294796824455261e-01 6.6191419959068298e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 409 1.9789366051554680e-03</internalNodes>
          <leafValues>
            7.5105965137481689e-02 -3.0839574337005615e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 244 6.4463824033737183e-02</internalNodes>
          <leafValues>
            2.0422630012035370e-02 -7.8423720598220825e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 208 2.5889080762863159e-01</internalNodes>
          <leafValues>
            2.0476030185818672e-02 -7.0666480064392090e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 386 -1.0318292770534754e-03</internalNodes>
          <leafValues>
            2.2414374351501465e-01 -8.8310293853282928e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 111 -1.7461649258621037e-04</internalNodes>
          <leafValues>
            1.4021448791027069e-01 -1.3769893348217010e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 67 -9.9463192746043205e-03</internalNodes>
          <leafValues>
            -2.2739125788211823e-01 8.5205666720867157e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 94 -3.6131145898252726e-03</internalNodes>
          <leafValues>
            -5.6930118799209595e-01 3.1317785382270813e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 151 7.0108915679156780e-04</internalNodes>
          <leafValues>
            4.1634697467088699e-02 -3.9024248719215393e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 134 2.2331513464450836e-03</internalNodes>
          <leafValues>
            -7.9074703156948090e-02 2.3458199203014374e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 373 6.3841314986348152e-03</internalNodes>
          <leafValues>
            -8.1743568181991577e-02 2.2234751284122467e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 408 -3.0848989263176918e-03</internalNodes>
          <leafValues>
            -3.2716140151023865e-01 5.8280918747186661e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 107 -1.2769144773483276e-01</internalNodes>
          <leafValues>
            -8.3935320377349854e-01 1.9475286826491356e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 172 -9.3862608075141907e-02</internalNodes>
          <leafValues>
            -8.1641745567321777e-01 1.7598237842321396e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 138 -2.3742191493511200e-02</internalNodes>
          <leafValues>
            2.3916700482368469e-01 -8.7493591010570526e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 369 6.1273737810552120e-04</internalNodes>
          <leafValues>
            -1.2326194345951080e-01 1.5700231492519379e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 295 -2.7675484307110310e-03</internalNodes>
          <leafValues>
            1.6751730442047119e-01 -1.1314858496189117e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 4 1.8545340746641159e-02</internalNodes>
          <leafValues>
            -1.3202618062496185e-01 1.4023675024509430e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 66 -6.3527323305606842e-02</internalNodes>
          <leafValues>
            4.3080195784568787e-01 -4.9772571772336960e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 13 1.7017025675158948e-04</internalNodes>
          <leafValues>
            9.5898360013961792e-02 -2.0378065109252930e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 13 -8.3076662849634886e-04</internalNodes>
          <leafValues>
            -3.6158534884452820e-01 5.4428659379482269e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 300 -5.8759599924087524e-03</internalNodes>
          <leafValues>
            2.3586516082286835e-01 -9.1378942131996155e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 280 2.4321996606886387e-03</internalNodes>
          <leafValues>
            -1.0467959195375443e-01 1.8839918076992035e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 132 -1.6474428121000528e-03</internalNodes>
          <leafValues>
            2.0396842062473297e-01 -9.7912020981311798e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 70 -2.6073291897773743e-02</internalNodes>
          <leafValues>
            -3.9660063385963440e-01 6.2811784446239471e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 245 3.3600386232137680e-03</internalNodes>
          <leafValues>
            5.0796363502740860e-02 -3.5952401161193848e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 347 -5.6270859204232693e-04</internalNodes>
          <leafValues>
            1.4142382144927979e-01 -1.3904143869876862e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 429 3.9613246917724609e-03</internalNodes>
          <leafValues>
            2.0853033289313316e-02 -8.4754186868667603e-01</leafValues></_></weakClassifiers></_>
    <!-- stage 14 -->
    <_>
      <maxWeakCount>57</maxWeakCount>
      <stageThreshold>-1.6956709623336792e+00</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>
            0 -1 222 1.1763212829828262e-01</internalNodes>
          <leafValues>
            -6.9316428899765015e-01 -2.9723501205444336e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 319 1.8279481679201126e-02</internalNodes>
          <leafValues>
            -2.9298681020736694e-01 7.4358269572257996e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 59 -2.9083793982863426e-02</internalNodes>
          <leafValues>
            1.4676998555660248e-01 -2.9355823993682861e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 404 -1.8593568820506334e-03</internalNodes>
          <leafValues>
            2.3336505889892578e-01 -9.9755316972732544e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 83 9.6774064004421234e-03</internalNodes>
          <leafValues>
            -8.7451040744781494e-02 2.4683545529842377e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 72 -6.8541448563337326e-03</internalNodes>
          <leafValues>
            3.3675724267959595e-01 -5.0646059215068817e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 368 -1.9490566104650497e-02</internalNodes>
          <leafValues>
            1.1184104532003403e-01 -2.5810897350311279e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 457 7.8681821469217539e-04</internalNodes>
          <leafValues>
            5.4076060652732849e-02 -3.9135706424713135e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 458 -7.5242517050355673e-04</internalNodes>
          <leafValues>
            -2.5969418883323669e-01 1.1135718226432800e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 87 -2.5853421539068222e-02</internalNodes>
          <leafValues>
            -4.9600359797477722e-01 4.7142092138528824e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 287 -4.0091353002935648e-04</internalNodes>
          <leafValues>
            -3.6486193537712097e-01 6.0857471078634262e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 354 3.1566455960273743e-02</internalNodes>
          <leafValues>
            4.5667488127946854e-02 -4.7117477655410767e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 425 -1.5358840115368366e-02</internalNodes>
          <leafValues>
            2.3615759611129761e-01 -1.0497896373271942e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 257 1.2973435223102570e-03</internalNodes>
          <leafValues>
            -9.8338156938552856e-02 2.3634901642799377e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 38 -2.1907091140747070e-02</internalNodes>
          <leafValues>
            3.3383834362030029e-01 -6.6575460135936737e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 257 -1.5134974382817745e-03</internalNodes>
          <leafValues>
            2.6111680269241333e-01 -8.8532261550426483e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 384 -4.2770290747284889e-03</internalNodes>
          <leafValues>
            -2.9896366596221924e-01 6.8718783557415009e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 394 1.4887228608131409e-02</internalNodes>
          <leafValues>
            -3.9886042475700378e-02 5.7147854566574097e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 117 -3.5248443600721657e-04</internalNodes>
          <leafValues>
            -3.0115553736686707e-01 6.7261718213558197e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 219 -1.8911302089691162e-02</internalNodes>
          <leafValues>
            -6.7464464902877808e-01 2.6777276769280434e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 175 4.2618028819561005e-02</internalNodes>
          <leafValues>
            -6.8460486829280853e-02 2.8744819760322571e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 231 -8.1339124590158463e-03</internalNodes>
          <leafValues>
            -6.6656559705734253e-01 3.2191168516874313e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 466 -3.6569873918779194e-04</internalNodes>
          <leafValues>
            -2.7597671747207642e-01 6.8382129073143005e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 466 2.6024243561550975e-04</internalNodes>
          <leafValues>
            8.4992490708827972e-02 -2.2100022435188293e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 427 -2.7046492323279381e-03</internalNodes>
          <leafValues>
            2.1760819852352142e-01 -8.7811328470706940e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 463 -4.4204322621226311e-03</internalNodes>
          <leafValues>
            -5.2971422672271729e-01 4.0565136820077896e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 444 1.5673721209168434e-02</internalNodes>
          <leafValues>
            -7.2288624942302704e-02 2.8392496705055237e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 476 -2.2519389167428017e-02</internalNodes>
          <leafValues>
            -3.5013788938522339e-01 5.5808387696743011e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 96 1.6242128913290799e-04</internalNodes>
          <leafValues>
            -2.5978651642799377e-01 7.3564678430557251e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 342 -1.7171478830277920e-03</internalNodes>
          <leafValues>
            2.9320308566093445e-01 -8.3711065351963043e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 343 -5.6327128550037742e-04</internalNodes>
          <leafValues>
            -2.9511910676956177e-01 7.6731510460376740e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 409 -7.1754015516489744e-04</internalNodes>
          <leafValues>
            -2.2248347103595734e-01 8.7633483111858368e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 282 -4.9601430073380470e-03</internalNodes>
          <leafValues>
            2.5491702556610107e-01 -8.6820304393768311e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 68 3.8469359278678894e-02</internalNodes>
          <leafValues>
            -1.2900568544864655e-01 1.9151265919208527e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 198 1.5056885313242674e-03</internalNodes>
          <leafValues>
            -1.7277084290981293e-01 1.3038231432437897e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 455 1.1067143641412258e-03</internalNodes>
          <leafValues>
            5.7108528912067413e-02 -3.3488905429840088e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 225 2.5329468771815300e-03</internalNodes>
          <leafValues>
            -7.7109865844249725e-02 2.5278598070144653e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 178 4.4696941040456295e-04</internalNodes>
          <leafValues>
            -1.8387977778911591e-01 1.1218409985303879e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 139 -2.9368935152888298e-02</internalNodes>
          <leafValues>
            3.8130557537078857e-01 -6.7904807627201080e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 250 -5.1710422849282622e-04</internalNodes>
          <leafValues>
            -2.1689635515213013e-01 9.7306318581104279e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 206 3.8344985805451870e-03</internalNodes>
          <leafValues>
            5.8058816939592361e-02 -3.4559842944145203e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 325 1.3030375121161342e-03</internalNodes>
          <leafValues>
            -6.9657169282436371e-02 2.8095620870590210e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 325 -4.9825810128822923e-04</internalNodes>
          <leafValues>
            2.3263372480869293e-01 -1.2029674649238586e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 3 8.9007552014663815e-04</internalNodes>
          <leafValues>
            8.2957021892070770e-02 -2.3670928180217743e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 152 8.3948709070682526e-03</internalNodes>
          <leafValues>
            3.4455027431249619e-02 -5.1275831460952759e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 51 1.5897378325462341e-02</internalNodes>
          <leafValues>
            -7.3407053947448730e-02 2.5420302152633667e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 401 -5.4110642522573471e-03</internalNodes>
          <leafValues>
            2.4382206797599792e-01 -7.8196465969085693e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 459 3.5087957512587309e-03</internalNodes>
          <leafValues>
            -8.4469787776470184e-02 2.2226931154727936e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 230 4.8821195377968252e-05</internalNodes>
          <leafValues>
            -2.1780093014240265e-01 8.9662902057170868e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 43 -1.2057019630447030e-03</internalNodes>
          <leafValues>
            1.8246965110301971e-01 -1.0304439812898636e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 52 2.5826733326539397e-04</internalNodes>
          <leafValues>
            7.7491052448749542e-02 -2.4328304827213287e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 395 3.9510201662778854e-02</internalNodes>
          <leafValues>
            4.5690886676311493e-02 -4.2056947946548462e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 436 -1.4117711689323187e-03</internalNodes>
          <leafValues>
            1.9540371000766754e-01 -9.9003188312053680e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 127 -2.5099519640207291e-02</internalNodes>
          <leafValues>
            -4.8088747262954712e-01 3.8761653006076813e-02</leafValues></_>
        <_>
          <internalNodes>
            0 -1 316 4.1705910116434097e-03</internalNodes>
          <leafValues>
            -7.9846158623695374e-02 2.6608175039291382e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 307 4.9760024994611740e-03</internalNodes>
          <leafValues>
            5.9690769761800766e-02 -3.2655736804008484e-01</leafValues></_>
        <_>
          <internalNodes>
            0 -1 61 1.7379848286509514e-03</internalNodes>
          <leafValues>
            -7.8966796398162842e-02 2.5055506825447083e-01</leafValues></_></weakClassifiers></_></stages>
  <features>
    <_>
      <rects>
        <_>
          0 0 1 2 -1.</_>
        <_>
          0 1 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 2 2 -1.</_>
        <_>
          0 0 1 1 2.</_>
        <_>
          1 1 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 2 2 -1.</_>
        <_>
          0 1 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 2 4 -1.</_>
        <_>
          0 1 2 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 4 20 -1.</_>
        <_>
          2 0 2 20 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 3 2 -1.</_>
        <_>
          0 1 3 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 4 2 -1.</_>
        <_>
          0 1 4 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 5 2 -1.</_>
        <_>
          0 1 5 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 12 2 -1.</_>
        <_>
          0 0 6 1 2.</_>
        <_>
          6 1 6 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 15 12 -1.</_>
        <_>
          0 6 15 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 0 17 4 -1.</_>
        <_>
          0 2 17 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 1 2 1 -1.</_>
        <_>
          1 1 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 1 20 4 -1.</_>
        <_>
          5 1 10 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 2 2 1 -1.</_>
        <_>
          1 2 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 2 3 6 -1.</_>
        <_>
          1 2 1 6 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 2 4 6 -1.</_>
        <_>
          0 2 2 3 2.</_>
        <_>
          2 5 2 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 4 2 10 -1.</_>
        <_>
          1 4 1 10 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 4 4 8 -1.</_>
        <_>
          2 4 2 8 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 4 8 10 -1.</_>
        <_>
          2 4 4 10 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 4 4 16 -1.</_>
        <_>
          2 4 2 16 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 4 4 9 -1.</_>
        <_>
          0 7 4 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 5 3 4 -1.</_>
        <_>
          1 5 1 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 5 2 7 -1.</_>
        <_>
          1 5 1 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 5 2 8 -1.</_>
        <_>
          1 5 1 8 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 5 4 9 -1.</_>
        <_>
          1 5 2 9 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 5 2 11 -1.</_>
        <_>
          1 5 1 11 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 5 11 3 -1.</_>
        <_>
          0 6 11 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 6 2 8 -1.</_>
        <_>
          1 6 1 8 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 6 4 11 -1.</_>
        <_>
          2 6 2 11 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 7 2 6 -1.</_>
        <_>
          1 7 1 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 7 20 4 -1.</_>
        <_>
          0 9 20 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 7 20 10 -1.</_>
        <_>
          0 12 20 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 9 2 8 -1.</_>
        <_>
          0 9 1 4 2.</_>
        <_>
          1 13 1 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 9 4 7 -1.</_>
        <_>
          1 9 2 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 10 3 4 -1.</_>
        <_>
          1 10 1 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 10 2 3 -1.</_>
        <_>
          0 11 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 10 3 4 -1.</_>
        <_>
          0 11 3 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 10 5 3 -1.</_>
        <_>
          0 11 5 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 11 4 9 -1.</_>
        <_>
          2 11 2 9 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 12 4 1 -1.</_>
        <_>
          1 12 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 12 4 3 -1.</_>
        <_>
          2 12 2 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 12 6 4 -1.</_>
        <_>
          2 12 2 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 12 6 8 -1.</_>
        <_>
          3 12 3 8 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 13 8 2 -1.</_>
        <_>
          2 13 4 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 13 6 5 -1.</_>
        <_>
          2 13 2 5 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 15 16 5 -1.</_>
        <_>
          4 15 8 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 16 2 3 -1.</_>
        <_>
          1 16 1 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 18 1 2 -1.</_>
        <_>
          0 19 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 18 2 2 -1.</_>
        <_>
          0 18 1 1 2.</_>
        <_>
          1 19 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 18 4 2 -1.</_>
        <_>
          0 19 4 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 18 10 2 -1.</_>
        <_>
          5 18 5 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          0 19 14 1 -1.</_>
        <_>
          7 19 7 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 0 2 2 -1.</_>
        <_>
          1 0 1 1 2.</_>
        <_>
          2 1 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 0 3 2 -1.</_>
        <_>
          1 1 3 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 0 12 1 -1.</_>
        <_>
          7 0 6 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 0 17 20 -1.</_>
        <_>
          1 5 17 10 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 0 18 20 -1.</_>
        <_>
          1 5 18 10 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 1 2 10 -1.</_>
        <_>
          1 1 1 5 2.</_>
        <_>
          2 6 1 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 4 16 3 -1.</_>
        <_>
          1 5 16 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 5 15 9 -1.</_>
        <_>
          6 5 5 9 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 5 12 3 -1.</_>
        <_>
          1 6 12 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 6 2 4 -1.</_>
        <_>
          1 6 1 2 2.</_>
        <_>
          2 8 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 6 6 14 -1.</_>
        <_>
          1 6 3 7 2.</_>
        <_>
          4 13 3 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 7 5 3 -1.</_>
        <_>
          1 8 5 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 8 4 12 -1.</_>
        <_>
          1 8 2 6 2.</_>
        <_>
          3 14 2 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          1 18 1 2 -1.</_>
        <_>
          1 19 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 0 2 14 -1.</_>
        <_>
          2 7 2 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 0 14 1 -1.</_>
        <_>
          9 0 7 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 0 13 4 -1.</_>
        <_>
          2 2 13 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 0 14 4 -1.</_>
        <_>
          2 2 14 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 1 9 4 -1.</_>
        <_>
          5 1 3 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 1 16 14 -1.</_>
        <_>
          2 1 8 7 2.</_>
        <_>
          10 8 8 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 3 3 2 -1.</_>
        <_>
          3 4 1 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          2 4 14 4 -1.</_>
        <_>
          9 4 7 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 5 2 1 -1.</_>
        <_>
          2 5 1 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          2 5 15 9 -1.</_>
        <_>
          7 5 5 9 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 8 2 2 -1.</_>
        <_>
          2 8 1 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          2 8 16 3 -1.</_>
        <_>
          6 8 8 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 8 12 5 -1.</_>
        <_>
          6 8 4 5 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 10 18 4 -1.</_>
        <_>
          11 10 9 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          2 19 8 1 -1.</_>
        <_>
          4 19 4 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 0 1 2 -1.</_>
        <_>
          3 1 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 0 13 4 -1.</_>
        <_>
          3 2 13 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 2 3 3 -1.</_>
        <_>
          4 3 1 3 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          3 5 12 9 -1.</_>
        <_>
          7 8 4 3 9.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 6 2 4 -1.</_>
        <_>
          4 6 1 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 6 8 10 -1.</_>
        <_>
          7 6 4 10 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 6 16 1 -1.</_>
        <_>
          11 6 8 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 6 12 2 -1.</_>
        <_>
          3 7 12 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 7 8 8 -1.</_>
        <_>
          7 7 4 8 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 7 15 6 -1.</_>
        <_>
          3 9 15 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 11 10 6 -1.</_>
        <_>
          8 11 5 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 12 1 4 -1.</_>
        <_>
          3 13 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 12 2 2 -1.</_>
        <_>
          3 12 1 1 2.</_>
        <_>
          4 13 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 13 3 1 -1.</_>
        <_>
          4 14 1 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          3 13 2 3 -1.</_>
        <_>
          3 14 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 13 10 3 -1.</_>
        <_>
          3 14 10 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 14 1 2 -1.</_>
        <_>
          3 15 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          3 15 8 4 -1.</_>
        <_>
          3 17 8 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 0 4 4 -1.</_>
        <_>
          4 0 2 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          4 0 4 10 -1.</_>
        <_>
          4 5 4 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 0 15 1 -1.</_>
        <_>
          9 0 5 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 0 6 3 -1.</_>
        <_>
          4 1 6 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 0 10 4 -1.</_>
        <_>
          4 2 10 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 0 15 20 -1.</_>
        <_>
          4 5 15 10 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 0 16 4 -1.</_>
        <_>
          4 2 16 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 1 7 2 -1.</_>
        <_>
          4 2 7 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 1 16 10 -1.</_>
        <_>
          4 1 8 5 2.</_>
        <_>
          12 6 8 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 1 11 2 -1.</_>
        <_>
          4 2 11 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 1 14 2 -1.</_>
        <_>
          4 2 14 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 4 3 4 -1.</_>
        <_>
          5 4 1 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 5 2 1 -1.</_>
        <_>
          5 5 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 7 12 7 -1.</_>
        <_>
          7 7 6 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 7 7 4 -1.</_>
        <_>
          3 8 7 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          4 9 10 6 -1.</_>
        <_>
          4 9 5 3 2.</_>
        <_>
          9 12 5 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 9 9 9 -1.</_>
        <_>
          4 12 9 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 10 3 2 -1.</_>
        <_>
          5 11 1 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          4 12 1 3 -1.</_>
        <_>
          4 13 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 12 2 2 -1.</_>
        <_>
          4 12 1 1 2.</_>
        <_>
          5 13 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 12 4 2 -1.</_>
        <_>
          4 12 2 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          4 12 16 8 -1.</_>
        <_>
          12 12 8 8 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 14 2 2 -1.</_>
        <_>
          4 14 1 1 2.</_>
        <_>
          5 15 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 14 12 4 -1.</_>
        <_>
          4 14 6 2 2.</_>
        <_>
          10 16 6 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 14 8 3 -1.</_>
        <_>
          4 15 8 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          4 15 12 4 -1.</_>
        <_>
          4 15 6 2 2.</_>
        <_>
          10 17 6 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 0 3 4 -1.</_>
        <_>
          6 1 1 4 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          5 0 3 5 -1.</_>
        <_>
          6 1 1 5 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          5 0 8 5 -1.</_>
        <_>
          7 0 4 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 0 9 6 -1.</_>
        <_>
          5 2 9 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 1 2 5 -1.</_>
        <_>
          5 1 1 5 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          5 1 3 5 -1.</_>
        <_>
          6 2 1 5 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          5 1 4 5 -1.</_>
        <_>
          6 2 2 5 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          5 1 3 4 -1.</_>
        <_>
          5 2 3 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 4 1 3 -1.</_>
        <_>
          5 5 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 5 3 3 -1.</_>
        <_>
          6 5 1 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 5 9 1 -1.</_>
        <_>
          8 5 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 5 12 6 -1.</_>
        <_>
          11 5 6 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 5 7 4 -1.</_>
        <_>
          4 6 7 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          5 6 10 6 -1.</_>
        <_>
          5 6 5 3 2.</_>
        <_>
          10 9 5 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 7 6 12 -1.</_>
        <_>
          5 11 6 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 8 4 6 -1.</_>
        <_>
          5 10 4 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 8 7 12 -1.</_>
        <_>
          5 11 7 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 9 3 1 -1.</_>
        <_>
          6 10 1 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          5 9 8 4 -1.</_>
        <_>
          5 11 8 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 11 1 4 -1.</_>
        <_>
          5 12 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 11 6 4 -1.</_>
        <_>
          5 13 6 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 12 3 1 -1.</_>
        <_>
          6 13 1 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          5 12 4 8 -1.</_>
        <_>
          5 14 4 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 13 1 4 -1.</_>
        <_>
          5 14 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 13 10 3 -1.</_>
        <_>
          5 14 10 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 14 1 3 -1.</_>
        <_>
          5 15 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 14 2 2 -1.</_>
        <_>
          5 14 1 1 2.</_>
        <_>
          6 15 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 14 13 2 -1.</_>
        <_>
          5 15 13 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          5 15 1 3 -1.</_>
        <_>
          5 16 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 0 4 6 -1.</_>
        <_>
          7 1 2 6 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          6 0 2 6 -1.</_>
        <_>
          6 2 2 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 0 8 2 -1.</_>
        <_>
          6 1 8 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 0 10 2 -1.</_>
        <_>
          6 1 10 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 1 9 7 -1.</_>
        <_>
          9 1 3 7 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 1 6 13 -1.</_>
        <_>
          9 1 3 13 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 1 5 8 -1.</_>
        <_>
          6 5 5 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 2 3 6 -1.</_>
        <_>
          6 2 3 3 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          6 2 8 10 -1.</_>
        <_>
          6 7 8 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 3 8 12 -1.</_>
        <_>
          6 6 8 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 4 6 4 -1.</_>
        <_>
          6 6 6 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 5 9 3 -1.</_>
        <_>
          9 5 3 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 5 4 4 -1.</_>
        <_>
          5 6 4 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          6 6 3 2 -1.</_>
        <_>
          7 6 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 6 2 3 -1.</_>
        <_>
          5 7 2 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          6 6 7 4 -1.</_>
        <_>
          5 7 7 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          6 7 5 6 -1.</_>
        <_>
          4 9 5 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          6 8 2 8 -1.</_>
        <_>
          7 8 1 8 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 8 9 3 -1.</_>
        <_>
          9 9 3 1 9.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 8 7 12 -1.</_>
        <_>
          6 12 7 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 9 1 4 -1.</_>
        <_>
          6 10 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 9 2 6 -1.</_>
        <_>
          4 11 2 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          6 10 10 10 -1.</_>
        <_>
          6 10 5 5 2.</_>
        <_>
          11 15 5 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 11 1 3 -1.</_>
        <_>
          6 12 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 11 3 3 -1.</_>
        <_>
          6 12 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 12 1 4 -1.</_>
        <_>
          6 13 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 12 12 8 -1.</_>
        <_>
          6 12 6 4 2.</_>
        <_>
          12 16 6 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 12 14 1 -1.</_>
        <_>
          13 12 7 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 13 3 2 -1.</_>
        <_>
          7 13 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 14 3 1 -1.</_>
        <_>
          7 15 1 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          6 14 3 2 -1.</_>
        <_>
          7 14 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 14 3 3 -1.</_>
        <_>
          6 15 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 16 1 2 -1.</_>
        <_>
          6 17 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          6 16 2 1 -1.</_>
        <_>
          6 16 1 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 0 2 7 -1.</_>
        <_>
          7 0 1 7 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 0 4 7 -1.</_>
        <_>
          7 0 2 7 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 0 4 2 -1.</_>
        <_>
          7 1 4 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 0 4 3 -1.</_>
        <_>
          7 1 4 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 0 4 4 -1.</_>
        <_>
          7 1 4 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 0 6 4 -1.</_>
        <_>
          7 1 6 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 0 9 6 -1.</_>
        <_>
          7 3 9 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 1 3 2 -1.</_>
        <_>
          7 2 3 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 1 3 3 -1.</_>
        <_>
          7 2 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 1 8 3 -1.</_>
        <_>
          7 2 8 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 2 2 6 -1.</_>
        <_>
          7 2 1 6 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 2 5 18 -1.</_>
        <_>
          7 11 5 9 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 3 6 6 -1.</_>
        <_>
          7 3 3 3 2.</_>
        <_>
          10 6 3 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 3 5 12 -1.</_>
        <_>
          7 6 5 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 3 5 12 -1.</_>
        <_>
          7 7 5 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 4 4 3 -1.</_>
        <_>
          8 4 2 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 4 4 3 -1.</_>
        <_>
          8 5 2 3 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 4 9 6 -1.</_>
        <_>
          10 4 3 6 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 4 4 3 -1.</_>
        <_>
          7 5 4 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 4 4 4 -1.</_>
        <_>
          7 5 4 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 4 9 14 -1.</_>
        <_>
          7 11 9 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 5 3 1 -1.</_>
        <_>
          8 5 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 5 4 1 -1.</_>
        <_>
          8 5 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 5 3 3 -1.</_>
        <_>
          8 5 1 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 5 2 3 -1.</_>
        <_>
          7 6 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 5 7 6 -1.</_>
        <_>
          5 7 7 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 5 8 6 -1.</_>
        <_>
          5 7 8 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 5 9 4 -1.</_>
        <_>
          6 6 9 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 6 2 3 -1.</_>
        <_>
          7 7 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 6 8 5 -1.</_>
        <_>
          7 6 4 5 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 6 5 4 -1.</_>
        <_>
          6 7 5 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 7 3 3 -1.</_>
        <_>
          8 8 1 3 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          7 8 12 6 -1.</_>
        <_>
          11 10 4 2 9.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 8 5 12 -1.</_>
        <_>
          7 12 5 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 9 9 6 -1.</_>
        <_>
          10 11 3 2 9.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 10 5 9 -1.</_>
        <_>
          7 13 5 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 11 1 4 -1.</_>
        <_>
          7 12 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 11 6 2 -1.</_>
        <_>
          7 11 3 1 2.</_>
        <_>
          10 12 3 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 11 4 3 -1.</_>
        <_>
          7 12 4 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 12 1 3 -1.</_>
        <_>
          7 13 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 12 2 3 -1.</_>
        <_>
          7 13 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 12 3 4 -1.</_>
        <_>
          7 13 3 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 14 3 3 -1.</_>
        <_>
          7 15 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 15 3 2 -1.</_>
        <_>
          7 16 3 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          7 16 2 2 -1.</_>
        <_>
          7 16 1 1 2.</_>
        <_>
          8 17 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 0 2 3 -1.</_>
        <_>
          8 1 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 0 2 4 -1.</_>
        <_>
          8 1 2 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 0 2 8 -1.</_>
        <_>
          8 0 2 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          8 0 6 5 -1.</_>
        <_>
          11 0 3 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 0 4 4 -1.</_>
        <_>
          8 1 4 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 0 8 4 -1.</_>
        <_>
          8 2 8 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 0 10 4 -1.</_>
        <_>
          8 2 10 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 1 2 2 -1.</_>
        <_>
          8 2 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 2 3 3 -1.</_>
        <_>
          9 2 1 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 2 12 17 -1.</_>
        <_>
          14 2 6 17 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 3 2 6 -1.</_>
        <_>
          8 5 2 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 3 8 14 -1.</_>
        <_>
          10 3 4 14 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 3 3 3 -1.</_>
        <_>
          8 4 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 3 8 1 -1.</_>
        <_>
          8 3 4 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          8 3 5 6 -1.</_>
        <_>
          6 5 5 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          8 3 5 8 -1.</_>
        <_>
          8 7 5 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 3 6 12 -1.</_>
        <_>
          8 6 6 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 4 3 3 -1.</_>
        <_>
          8 5 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 4 9 14 -1.</_>
        <_>
          11 4 3 14 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 4 5 4 -1.</_>
        <_>
          8 5 5 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 5 3 2 -1.</_>
        <_>
          9 5 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 5 4 2 -1.</_>
        <_>
          9 5 2 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 5 2 5 -1.</_>
        <_>
          9 5 1 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 5 6 6 -1.</_>
        <_>
          6 7 6 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          8 6 3 2 -1.</_>
        <_>
          9 6 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 6 3 12 -1.</_>
        <_>
          8 10 3 4 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 6 8 4 -1.</_>
        <_>
          7 7 8 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          8 7 1 12 -1.</_>
        <_>
          8 10 1 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 7 4 9 -1.</_>
        <_>
          8 10 4 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 7 5 2 -1.</_>
        <_>
          8 8 5 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 7 12 2 -1.</_>
        <_>
          14 7 6 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 8 3 9 -1.</_>
        <_>
          8 11 3 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 8 5 8 -1.</_>
        <_>
          8 10 5 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 9 2 4 -1.</_>
        <_>
          8 10 2 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 9 2 8 -1.</_>
        <_>
          8 11 2 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 9 3 8 -1.</_>
        <_>
          8 11 3 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 10 2 4 -1.</_>
        <_>
          8 12 2 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 11 4 4 -1.</_>
        <_>
          8 12 4 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 12 1 3 -1.</_>
        <_>
          8 13 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 13 1 3 -1.</_>
        <_>
          8 14 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 13 3 6 -1.</_>
        <_>
          9 13 1 6 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 14 1 3 -1.</_>
        <_>
          8 15 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 14 2 3 -1.</_>
        <_>
          8 15 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 14 3 3 -1.</_>
        <_>
          8 15 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 16 2 2 -1.</_>
        <_>
          8 17 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 17 3 1 -1.</_>
        <_>
          9 17 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          8 17 3 2 -1.</_>
        <_>
          8 18 3 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 0 2 3 -1.</_>
        <_>
          9 1 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 1 2 9 -1.</_>
        <_>
          9 1 1 9 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          9 1 5 2 -1.</_>
        <_>
          9 2 5 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 2 6 8 -1.</_>
        <_>
          9 2 3 8 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          9 3 1 3 -1.</_>
        <_>
          9 4 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 3 4 3 -1.</_>
        <_>
          10 3 2 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 3 3 4 -1.</_>
        <_>
          9 4 3 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 3 6 3 -1.</_>
        <_>
          9 3 3 3 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          9 4 3 1 -1.</_>
        <_>
          10 4 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 4 3 2 -1.</_>
        <_>
          10 4 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 4 3 6 -1.</_>
        <_>
          9 6 3 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 5 4 8 -1.</_>
        <_>
          9 5 4 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          9 6 3 4 -1.</_>
        <_>
          9 8 3 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 6 4 6 -1.</_>
        <_>
          9 8 4 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 7 3 1 -1.</_>
        <_>
          10 7 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 7 8 1 -1.</_>
        <_>
          11 9 4 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          9 7 9 2 -1.</_>
        <_>
          12 10 3 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          9 7 8 3 -1.</_>
        <_>
          9 8 8 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 8 2 4 -1.</_>
        <_>
          9 9 2 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 8 8 1 -1.</_>
        <_>
          11 10 4 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          9 8 3 3 -1.</_>
        <_>
          9 9 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 11 2 1 -1.</_>
        <_>
          10 11 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 11 2 3 -1.</_>
        <_>
          9 12 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 12 1 4 -1.</_>
        <_>
          9 13 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 13 2 4 -1.</_>
        <_>
          9 14 2 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 14 1 3 -1.</_>
        <_>
          9 15 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 14 2 2 -1.</_>
        <_>
          9 14 1 1 2.</_>
        <_>
          10 15 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 14 3 3 -1.</_>
        <_>
          10 15 1 1 9.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 14 2 3 -1.</_>
        <_>
          9 15 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 15 1 3 -1.</_>
        <_>
          9 16 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 15 3 2 -1.</_>
        <_>
          10 15 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 16 1 2 -1.</_>
        <_>
          9 17 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 16 3 1 -1.</_>
        <_>
          10 16 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 16 2 2 -1.</_>
        <_>
          9 16 1 1 2.</_>
        <_>
          10 17 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          9 17 10 2 -1.</_>
        <_>
          14 17 5 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 0 1 10 -1.</_>
        <_>
          10 0 1 5 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          10 0 3 6 -1.</_>
        <_>
          11 0 1 6 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 0 3 3 -1.</_>
        <_>
          10 1 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 0 7 4 -1.</_>
        <_>
          10 2 7 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 0 10 4 -1.</_>
        <_>
          10 2 10 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 1 6 3 -1.</_>
        <_>
          10 1 3 3 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          10 1 10 17 -1.</_>
        <_>
          15 1 5 17 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 2 6 3 -1.</_>
        <_>
          9 3 6 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          10 3 4 8 -1.</_>
        <_>
          10 3 2 8 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          10 4 4 1 -1.</_>
        <_>
          11 4 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 5 3 1 -1.</_>
        <_>
          11 5 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 5 3 4 -1.</_>
        <_>
          10 7 3 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 5 6 6 -1.</_>
        <_>
          13 5 3 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 6 3 1 -1.</_>
        <_>
          11 6 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 6 3 2 -1.</_>
        <_>
          11 7 1 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          10 6 2 9 -1.</_>
        <_>
          10 9 2 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 7 3 2 -1.</_>
        <_>
          10 8 3 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 8 1 4 -1.</_>
        <_>
          10 9 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 8 1 4 -1.</_>
        <_>
          10 10 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 8 2 8 -1.</_>
        <_>
          10 10 2 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 9 1 4 -1.</_>
        <_>
          10 10 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 9 3 4 -1.</_>
        <_>
          10 10 3 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 9 4 4 -1.</_>
        <_>
          10 10 4 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 9 5 6 -1.</_>
        <_>
          10 9 5 3 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          10 11 1 4 -1.</_>
        <_>
          10 12 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 12 1 3 -1.</_>
        <_>
          10 13 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 13 1 3 -1.</_>
        <_>
          10 14 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 13 2 2 -1.</_>
        <_>
          10 14 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 14 3 3 -1.</_>
        <_>
          10 15 3 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 15 1 2 -1.</_>
        <_>
          10 16 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 15 2 2 -1.</_>
        <_>
          10 15 1 1 2.</_>
        <_>
          11 16 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 16 1 2 -1.</_>
        <_>
          10 17 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          10 17 1 2 -1.</_>
        <_>
          10 18 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 4 2 2 -1.</_>
        <_>
          12 4 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 4 4 2 -1.</_>
        <_>
          12 4 2 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 5 4 1 -1.</_>
        <_>
          12 5 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 5 4 8 -1.</_>
        <_>
          11 5 4 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          11 6 6 8 -1.</_>
        <_>
          11 6 6 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          11 8 1 6 -1.</_>
        <_>
          11 8 1 3 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          11 8 6 3 -1.</_>
        <_>
          14 8 3 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 8 4 8 -1.</_>
        <_>
          11 10 4 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 9 2 2 -1.</_>
        <_>
          11 10 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 9 2 3 -1.</_>
        <_>
          11 10 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 10 8 2 -1.</_>
        <_>
          13 12 4 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          11 14 3 3 -1.</_>
        <_>
          12 14 1 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 15 1 2 -1.</_>
        <_>
          11 16 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          11 15 3 1 -1.</_>
        <_>
          12 15 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          12 0 1 3 -1.</_>
        <_>
          12 1 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          12 3 2 10 -1.</_>
        <_>
          12 3 1 10 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          12 3 4 5 -1.</_>
        <_>
          12 3 2 5 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          12 5 3 1 -1.</_>
        <_>
          13 6 1 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          12 5 3 4 -1.</_>
        <_>
          13 6 1 4 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          12 5 6 5 -1.</_>
        <_>
          15 5 3 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          12 5 6 8 -1.</_>
        <_>
          12 5 6 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          12 9 1 4 -1.</_>
        <_>
          12 10 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          12 9 2 3 -1.</_>
        <_>
          12 10 2 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          12 11 3 1 -1.</_>
        <_>
          13 12 1 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          12 15 1 2 -1.</_>
        <_>
          12 16 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          12 17 6 3 -1.</_>
        <_>
          14 17 2 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          13 0 2 2 -1.</_>
        <_>
          13 0 2 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 0 7 2 -1.</_>
        <_>
          13 0 7 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 1 4 11 -1.</_>
        <_>
          13 1 2 11 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 3 6 3 -1.</_>
        <_>
          15 4 2 1 9.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          13 5 3 1 -1.</_>
        <_>
          14 6 1 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 5 1 9 -1.</_>
        <_>
          10 8 1 3 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 5 2 8 -1.</_>
        <_>
          11 7 2 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 6 6 5 -1.</_>
        <_>
          15 6 2 5 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          13 6 6 8 -1.</_>
        <_>
          13 6 6 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 7 6 4 -1.</_>
        <_>
          15 9 2 4 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 12 1 6 -1.</_>
        <_>
          13 12 1 3 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 12 6 2 -1.</_>
        <_>
          15 14 2 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          13 18 2 2 -1.</_>
        <_>
          14 18 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          14 0 6 2 -1.</_>
        <_>
          14 0 6 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          14 0 6 3 -1.</_>
        <_>
          13 1 6 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          14 2 2 10 -1.</_>
        <_>
          14 2 2 5 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          14 4 3 2 -1.</_>
        <_>
          15 5 1 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          14 4 6 16 -1.</_>
        <_>
          17 4 3 16 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          14 5 6 14 -1.</_>
        <_>
          17 5 3 14 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          14 6 4 8 -1.</_>
        <_>
          14 6 4 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          14 7 2 7 -1.</_>
        <_>
          14 7 1 7 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          14 9 6 6 -1.</_>
        <_>
          14 12 6 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          14 11 6 2 -1.</_>
        <_>
          16 11 2 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          14 11 6 3 -1.</_>
        <_>
          16 11 2 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          14 16 2 2 -1.</_>
        <_>
          14 16 1 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          15 0 4 3 -1.</_>
        <_>
          14 1 4 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          15 1 5 3 -1.</_>
        <_>
          14 2 5 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          15 2 4 6 -1.</_>
        <_>
          16 2 2 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          15 5 3 1 -1.</_>
        <_>
          16 6 1 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          15 6 4 1 -1.</_>
        <_>
          16 6 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          15 7 2 4 -1.</_>
        <_>
          15 7 1 2 2.</_>
        <_>
          16 9 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          15 9 4 4 -1.</_>
        <_>
          16 9 2 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          15 10 4 5 -1.</_>
        <_>
          16 11 2 5 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          15 14 3 3 -1.</_>
        <_>
          16 15 1 3 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          15 18 5 2 -1.</_>
        <_>
          15 19 5 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 0 4 2 -1.</_>
        <_>
          16 1 4 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 0 4 4 -1.</_>
        <_>
          16 0 4 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          16 4 1 2 -1.</_>
        <_>
          16 4 1 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          16 4 4 2 -1.</_>
        <_>
          16 4 2 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          16 4 4 10 -1.</_>
        <_>
          18 4 2 10 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 5 3 3 -1.</_>
        <_>
          17 5 1 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 5 4 9 -1.</_>
        <_>
          18 5 2 9 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 6 3 2 -1.</_>
        <_>
          17 6 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 6 4 4 -1.</_>
        <_>
          18 6 2 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 6 4 6 -1.</_>
        <_>
          18 6 2 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 6 4 7 -1.</_>
        <_>
          18 6 2 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 8 3 2 -1.</_>
        <_>
          17 8 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 8 4 7 -1.</_>
        <_>
          18 8 2 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 9 4 5 -1.</_>
        <_>
          17 10 2 5 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          16 9 3 6 -1.</_>
        <_>
          17 10 1 6 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          16 10 4 6 -1.</_>
        <_>
          17 11 2 6 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          16 10 4 4 -1.</_>
        <_>
          18 10 2 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 10 4 6 -1.</_>
        <_>
          16 10 2 6 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          16 11 4 2 -1.</_>
        <_>
          17 11 2 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 11 4 5 -1.</_>
        <_>
          17 12 2 5 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          16 12 1 3 -1.</_>
        <_>
          16 13 1 1 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          16 12 4 4 -1.</_>
        <_>
          16 12 2 4 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 0 1 2 -1.</_>
        <_>
          17 1 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          17 1 2 13 -1.</_>
        <_>
          18 1 1 13 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          17 4 3 2 -1.</_>
        <_>
          17 4 3 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 5 2 7 -1.</_>
        <_>
          18 5 1 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          17 6 2 1 -1.</_>
        <_>
          18 6 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          17 6 3 2 -1.</_>
        <_>
          18 6 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          17 8 2 1 -1.</_>
        <_>
          18 8 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          17 9 3 2 -1.</_>
        <_>
          18 9 1 2 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          17 9 3 2 -1.</_>
        <_>
          18 10 1 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 9 3 3 -1.</_>
        <_>
          18 9 1 3 3.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          17 10 3 7 -1.</_>
        <_>
          18 11 1 7 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 10 2 6 -1.</_>
        <_>
          17 10 2 3 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 11 3 4 -1.</_>
        <_>
          18 12 1 4 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 11 3 6 -1.</_>
        <_>
          18 12 1 6 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 11 2 6 -1.</_>
        <_>
          15 13 2 2 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 12 3 4 -1.</_>
        <_>
          18 13 1 4 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 12 3 5 -1.</_>
        <_>
          18 13 1 5 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 12 2 3 -1.</_>
        <_>
          16 13 2 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 13 2 3 -1.</_>
        <_>
          17 13 1 3 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          17 13 3 3 -1.</_>
        <_>
          18 14 1 3 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          18 0 2 1 -1.</_>
        <_>
          19 0 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 0 2 2 -1.</_>
        <_>
          18 0 1 1 2.</_>
        <_>
          19 1 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 0 2 2 -1.</_>
        <_>
          19 0 1 2 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 0 2 3 -1.</_>
        <_>
          19 0 1 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 0 2 2 -1.</_>
        <_>
          18 1 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 0 2 16 -1.</_>
        <_>
          14 4 2 8 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          18 1 2 1 -1.</_>
        <_>
          19 1 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 1 2 3 -1.</_>
        <_>
          19 1 1 3 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 2 1 3 -1.</_>
        <_>
          17 3 1 1 3.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          18 5 2 11 -1.</_>
        <_>
          19 5 1 11 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 6 2 7 -1.</_>
        <_>
          19 6 1 7 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 8 2 5 -1.</_>
        <_>
          19 8 1 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 11 1 2 -1.</_>
        <_>
          18 11 1 1 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          18 11 2 4 -1.</_>
        <_>
          18 11 2 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          18 12 2 6 -1.</_>
        <_>
          18 12 1 6 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          18 18 2 1 -1.</_>
        <_>
          19 18 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 18 1 2 -1.</_>
        <_>
          18 19 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 18 2 2 -1.</_>
        <_>
          18 18 1 1 2.</_>
        <_>
          19 19 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          18 18 2 2 -1.</_>
        <_>
          18 19 2 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          19 0 1 2 -1.</_>
        <_>
          19 1 1 1 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          19 0 1 18 -1.</_>
        <_>
          19 9 1 9 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          19 1 1 4 -1.</_>
        <_>
          19 1 1 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          19 1 1 10 -1.</_>
        <_>
          19 6 1 5 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          19 1 1 12 -1.</_>
        <_>
          19 7 1 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          19 3 1 4 -1.</_>
        <_>
          19 3 1 2 2.</_></rects>
      <tilted>1</tilted></_>
    <_>
      <rects>
        <_>
          19 5 1 12 -1.</_>
        <_>
          19 11 1 6 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          19 12 1 8 -1.</_>
        <_>
          19 16 1 4 2.</_></rects>
      <tilted>0</tilted></_>
    <_>
      <rects>
        <_>
          19 18 1 2 -1.</_>
        <_>
          19 19 1 1 2.</_></rects>
      <tilted>0</tilted></_></features></cascade>
</opencv_storage>
"""


class GestureRecognition(rumps.App):
	def __init__(self, name):
		rumps.App.__init__(self, name)
		self.t = threading.Thread(target=self.detecting)
		self.t.start()
		print(self.resource_path("fist.xml"))
		newfile = open(self.resource_path("fist.xml"),"w+")
		for line in XMLDOCFIST:
			newfile.write(line)
		newfile.close()
		self.fist_cascade = cv2.CascadeClassifier(self.resource_path("fist.xml"))
		if os.popen("""osascript -e 'application "Spotify" is running' """).read().strip() == 'true':
			self.app_control = "Spotify"
		elif os.popen("""osascript -e 'application "iTunes" is running' """).read().strip() == 'true':
			self.app_control = "iTunes"
		else:
			os.system("""osascript -e 'tell application "iTunes" to activate'""")
			self.app_control = "iTunes"
		#rumps.notification("Voleter", "Now Controlling {}".format(self.app_control), "To toggle playback of this app, make a fist in front of your webcam.")

	def resource_path(self, relative_path): # needed for bundling
	    """ Get absolute path to resource, works for dev and for PyInstaller """
	    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	    return os.path.join(base_path, relative_path)

	def detecting(self):
	    self.video_capture = cv2.VideoCapture(0)
	    while True:
	      _, frame = self.video_capture.read()
	      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	      canvas = self.detect(gray, frame)
	      if not self.video_capture:
	          break
	    video_capture.release()
	    cv2.destroyAllWindows()

	def detect(self, gray, frame):
	  fists = self.fist_cascade.detectMultiScale(gray, 1.3, 5)
	  if len(fists) != 0:
	      os.system(TOGGLE_OSASCRIPT.format(self.app_control, self.app_control, self.app_control, self.app_control))
	      time.sleep(2)
	  return frame

	@rumps.clicked("Control Spotify")
	def spotify(self, _):
	    #rumps.notification("Voleter", "Now Controlling Spotify", "To toggle playback of this app, make a fist in front of your webcam.")
	    self.app_control = 'Spotify'

	@rumps.clicked("Control iTunes")
	def iTunes(self, _):
	    #rumps.notification("Voleter", "Now Controlling iTunes", "To toggle playback of this app, make a fist in front of your webcam.")
	    self.app_control = 'iTunes'

if __name__ == "__main__":
    GestureRecognition(name="Voleter").run()
