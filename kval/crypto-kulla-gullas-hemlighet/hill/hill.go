package hill

import (
	"errors"
	"fmt"
	"math/rand"
)

func Genkey(n, mod int) [][]int {
	var key [][]int
	for i := 0; i < n; i++ {
		var row []int
		for j := 0; j < n; j++ {
			row = append(row, rand.Int()%mod)
		}
		key = append(key, row)
	}
	return key
}

func Encrypt(p []int, key [][]int, mod int) []int {
	n := len(key)
	if x := len(p) % n; x != 0 {
		fmt.Printf("Bad p length! p: %d p%%n: %d\n", len(p), x)
		return nil
	}
	var c []int
	for i := 0; i < len(p); i += n {
		for j := 0; j < n; j++ {
			r := 0
			for k := 0; k < n; k++ {
				r = (r + key[j][k]*p[i+k]) % mod
			}
			c = append(c, r)
		}
	}
	return c
}

// egcd calculates the extended euclidean algorithm.
// ax + by = g = gcd(a, b)
func egcd(a, b int) (g, x, y int) {
	x0, x1, y0, y1 := 0, 1, 1, 0
	for a != 0 {
		q := b / a
		b, a = a, b-q*a
		y0, y1 = y1, y0-q*y1
		x0, x1 = x1, x0-q*x1
	}
	return b, x0, y0
}

func modinv(a, b int) (int, error) {
	g, x, _ := egcd(a, b)
	if g != 1 {
		return 0, fmt.Errorf("gcd is not 1: %d", g)
	}
	for x < 0 {
		x += b
	}
	return x % b, nil
}

func unit(n int) [][]int {
	var m [][]int
	for r := 0; r < n; r++ {
		var t []int
		for c := 0; c < n; c++ {
			if r == c {
				t = append(t, 1)
			} else {
				t = append(t, 0)
			}
		}
		m = append(m, t)
	}
	return m
}

func printMatrix(key, res [][]int) {
	n := len(key)
	for r := 0; r < n; r++ {
		for _, n := range key[r] {
			fmt.Printf("%2d ", n)
		}
		fmt.Printf(" | ")
		for _, n := range res[r] {
			fmt.Printf("%2d ", n)
		}
		fmt.Println("")
	}
}

func InvertMatrix(key [][]int, mod int) ([][]int, error) {
	n := len(key)
	res := unit(n)
	columnsReduced := make([]bool, n)
	rowsReduced := make([]bool, n)
	for laps := 0; laps < n; laps++ {
		rowToPick := -1
		colToPick := -1
		minv := 0
		for c := 0; c < n && rowToPick == -1; c++ {
			if columnsReduced[c] {
				continue
			}
			for r := 0; r < n; r++ {
				if rowsReduced[r] {
					continue
				}
				var err error
				minv, err = modinv(key[r][c], mod)
				if err == nil {
					rowToPick = r
					colToPick = c
					break
				}
			}
		}
		if rowToPick == -1 {
			return nil, errors.New("key is not invertible")
		}
		rowsReduced[rowToPick] = true
		columnsReduced[colToPick] = true

		for c := 0; c < n; c++ {
			key[rowToPick][c] = (key[rowToPick][c] * minv) % mod
			res[rowToPick][c] = (res[rowToPick][c] * minv) % mod
		}

		for r := 0; r < n; r++ {
			if r == rowToPick {
				continue
			}
			keyRCol := key[r][colToPick]
			for c := 0; c < n; c++ {
				key[r][c] = (key[r][c] - keyRCol*key[rowToPick][c] + mod*mod) % mod
				res[r][c] = (res[r][c] - keyRCol*res[rowToPick][c] + mod*mod) % mod
			}
		}
	}

	// shift rows to the right place
	for c := 0; c < n; c++ {
		for r := 0; r < n; r++ {
			if key[r][c] != 1 || r == c {
				continue
			}
			key[r], key[c] = key[c], key[r]
			res[r], res[c] = res[c], res[r]
		}
	}

	return res, nil
}

func Decrypt(c []int, key [][]int, mod int) ([]int, error) {
	invKey, err := InvertMatrix(key, mod)
	if err != nil {
		return nil, err
	}
	return Encrypt(c, invKey, mod), nil
}

func indexRune(needle rune, haystack []rune) int {
	for i, h := range haystack {
		if needle == h {
			return i
		}
	}
	return -1
}

func DecodeAlphabet(p []rune, alphabet []rune) []int {
	var res []int
	for _, r := range p {
		res = append(res, indexRune(r, alphabet))
	}
	return res
}

func EncodeAlphabet(c []int, alphabet []rune) []rune {
	var res []rune
	for _, cc := range c {
		res = append(res, alphabet[cc])
	}
	return res
}
