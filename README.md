# How Fair are Major League Ball Parks?

## About

In the Fall of 2003 I participated in the [COMAP's HiMCM][0] (High School Mathematical Competition in Modeling).  In this competition we were given 36 hours to write up a solution the following question:

> Consider the following major league baseball parks: Atlanta Braves, Colorado Rockies, New York Yankees, California Angles, Minnesota Twins, and Florida Marlins.  Each field is in a different location and has different dimensions. Are all these parks "fair"? Determine how fair or unfair is each park. Determine the optimal baseball "setting" for major league baseball.

My team addressed this with a simulation.  We simulated the trajectory of a batted ball (where the pitch speed, bat speed and ball direction were random variables) for 1000 batters in each park.  We can use this as a metric for fairness.  We decided a park would be fair if a batted ball was equally likely to go out regardless which direction it was hit.  We designed a park accordingly.

Our paper was ranked as "nationally outstanding" and published.  Only 9 of the submissions 274 received this mark.  It is available [here][1] (go to page 36 of the pdf).

I have recently recast the original C++ program in Python and have also addressed this same question using data analytic and sabermetric techniques (though this last part is still a work in progress).  I have not addressed the last part of the orriginal question (regarding the optimal baseball settings) in this recasting (as it is less interesting to me).

## Usage

Simply run `./main <fields.txt` to execute the program, where `fields.txt` contains each ballpark the park's name, dimensions, wall heights, and
air resistance. Use `-n` to specify the number of at-bats per ballpark (defaults to 1000).

[0]: http://www.comap.com/highschool/contests/himcm/
[1]: https://dl.dropboxusercontent.com/u/1444851/Website/Cons86.pdf