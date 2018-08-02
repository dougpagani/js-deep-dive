/*

const x = {
    foo: 123,
    bar: 432,
};

x.late = 'hello';
console.log('x', x);

const y = Object.create(x);
y.otherlate = 'yeye';

console.log('y', y);

console.log('y.foo:', y.foo);
console.log("y's prototype:", Object.getPrototypeOf(y));
console.log("x's prototype:", Object.getPrototypeOf(x));

x.asdf = 'new after Y';
console.log("y's prototype:", Object.getPrototypeOf(y));

*/
/*

const a = [5 ,4 ,33];

const aobj = {
    0: 5,
    1: 4,
    2: 33,
};
Object.setPrototypeOf(aobj, Object.getPrototypeOf(a));

const b = a.map(x => x * 2);

console.log('a', a);
console.log('aobj', aobj);
console.log('b', b);

console.log(a['0'])
console.log(aobj[ 0 ])

console.log(Array.prototype === Object.getPrototypeOf(a))
console.log(Object.getPrototypeOf([]))
console.log(Array.prototype == [])
console.log(Array.prototype == [])

// [] <==>
// (a = {}; Object.setPrototypeOf(a, Array.prototype) )

collectionOfUsefulArrayMethodsAndStuff = {
    prototype: Object.getPrototypeOf([]),
};

Array = {
    prototype: Object.getPrototypeOf([]),
};
*/
/*

// [].prototype

function foo(x, y) {
    return x + y;
}

console.log(foo(3, 3));

console.log(foo.prototype);

// function foo() {} 
// foo.prototype
// foo.prototype.x = 123;


Object.create(x)
// <===>
(a = {}; Object.setPrototypeOf(a, x); return a);

// whence (= where from) cometh the .prototype? every time you create a
// function:
function asdf() {                       
}                                       
// javascript will immediately:         
//asdf.prototype = { constructor: asdf};
                                        
//because now:                          
const x = new asdf();                   
// which is syntactic sugar for:        
const x = Object.create(asdf.prototype);
asdf(x); // (sort of)                   
// which, in turn, is syntactic sugar for:
const x = {};
Object.setPrototypeOf(x, asdf);
asdf(x); // again, sort of

*/

/*
!!!!"this";


function myfun(a, b) {
    //console.log('this:', this, a, b);
    console.log( a, b);
}


myfun.call(undefined, 1, 2);
// <=>
// {oldthis=this; this=undefined; myfun(2); this=oldthis;}
myfun.call(1, 2);
// <=>
// {oldthis=this; this=1; myfun(2); this=oldthis;}

const x = new asdf();
//note:
Object.getPrototypeOf(x).constructor === asdf; // keep in mind!

const foo = new Foozer();
foo.bar(1, 2);
// <=>
// Object.getPrototypeOf(foo).prototype.bar.call(foo, 1, 2);
// <=>
// Foozer.prototype.bar.call(foo, 1, 2);

// so what's the point? well:

*/

/*
function Foozer() {};
Foozer.prototype.bar = function () {
    const i_am_foo = this; // !!!!
    console.log(i_am_foo);
}

const foo = new Foozer();

foo.y = 'I am foo.y';

foo.bar();

*/

"constructors"; // in quotes

function Doozer(x) {
    console.log(this); // what am I???
    console.log(Object.getPrototypeOf(this).constructor === Doozer);
    this.y = x; // who is this???


    // what would happen if I did this?
    //return {a: 'whhaaat?'};
}

// don't forget: we declared a function, so Javascript has secretly created a
// fresh object with one hidden key (constructor) and assigned the function
// (Doozer) to it:
//Doozer.prototype = { constructor: Doozer };
// I.e.:
console.log('check:', Doozer === Doozer.prototype.constructor);



const zim = new Doozer(3);
// <=>
// const zim = Object.create(Doozer.prototype);
// Doozer.call(zim, 3);
// <=>
// const zim = {};
// Object.setPrototypeOf(zim, Doozer.prototype);
// Doozer.call(zim, 3);



// Again:
function Point(x, y) {
    this.x = x;
    this.y = y;
}

const globalthis = (function () { return this; })();

// So now that we have a (automatically created) (but also pretty empty, by
// default) prototype object, let's:
Point.prototype.mylen = function () {
    if (this === globalthis) {
        console.log( "this not set to a point instance; set to globalthis!");
    } else {
        console.log(this);
    }
    return Math.pow(this.x * this.y, 0.5);
}


const p1 = new Point(1, 2);
p1.name = 'p1';
const p2 = new Point(3, 3);
p2.name = 'p2';
const p3 = new Point(0, 0);
p3.name = 'p3';

const points = [p1, p2, p3];

const lengths = points.map(point => point.mylen());
console.log(lengths);
