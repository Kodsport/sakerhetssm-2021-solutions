package main

import (
	"fmt"
	"math/rand"

	"github.com/sakerhetssm-2021/kval/crypto-kulla-gullas-hemlighet/hill"
)

func main() {
	const n int = 2
	var alphabet = []rune("ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ")
	var p = []rune("MITTCHIFFERÄRBÄTTREÄNDITTLESTERMVHKG")

	rand.Seed(1337)
	mod := len(alphabet)
	fmt.Printf("n: %d\n", n)
	var key [][]int
	for true {
		key = hill.Genkey(n, mod) // TODO: assert that key is invertible

		var k [][]int
		for r := 0; r < n; r++ {
			x := make([]int, n)
			copy(x, key[r])
			k = append(k, x)
		}
		if _, err := hill.InvertMatrix(k, mod); err == nil {
			break
		}
	}

	/*
		fmt.Printf("KEY:\n")
		for r := 0; r < n; r++ {
			for c := 0; c < n; c++ {
				fmt.Printf("%2d ", key[r][c])
			}
			fmt.Println()
		}
	*/

	px := hill.DecodeAlphabet(p, alphabet)
	// fmt.Printf("px: %v\n", px)
	cx := hill.Encrypt(px, key, mod)
	// fmt.Printf("cx: %v\n", cx)
	c := hill.EncodeAlphabet(cx, alphabet)
	fmt.Printf("c: %s\n", string(c))

	pp, err := hill.Decrypt(cx, key, mod)
	if err != nil {
		panic(err)
	}
	for i := 0; i < len(px); i++ {
		if pp[i] != px[i] {
			panic("bad")
		}
	}
}
