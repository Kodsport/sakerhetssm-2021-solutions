package hill

import (
	"testing"

	"github.com/google/go-cmp/cmp"
)

func TestEncrypt(t *testing.T) {
	tests := []struct {
		name string
		mod  int
		p    []int
		key  [][]int
		c    []int
	}{
		{
			name: "Invalid size of p",
			p:    []int{1, 2, 3},
			key:  [][]int{{22, 13}, {7, 23}},
		},
		{
			name: "Wikipedia 1",
			mod:  26,
			p:    []int{0, 2, 19},
			key: [][]int{
				{6, 24, 1},
				{13, 16, 10},
				{20, 17, 15},
			},
			c: []int{15, 14, 7},
		},
		{
			name: "Wikipedia 2",
			mod:  26,
			p:    []int{2, 0, 19},
			key: [][]int{
				{6, 24, 1},
				{13, 16, 10},
				{20, 17, 15},
			},
			c: []int{5, 8, 13},
		},
		{
			name: "Wikipedia 3",
			mod:  26,
			p:    []int{7, 4},
			key: [][]int{
				{3, 3},
				{2, 5},
			},
			c: []int{7, 8},
		},
		{
			name: "Wikipedia 4",
			mod:  26,
			p:    []int{11, 15},
			key: [][]int{
				{3, 3},
				{2, 5},
			},
			c: []int{0, 19},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := Encrypt(tt.p, tt.key, tt.mod)
			if diff := cmp.Diff(tt.c, got); diff != "" {
				t.Errorf("Encrypt() mismatch (-want +got):\n%s", diff)
			}
		})
	}
}

func TestDecrypt(t *testing.T) {
	tests := []struct {
		name string
		mod  int
		c    []int
		key  [][]int
		p    []int
	}{
		{
			name: "Wikipedia 1",
			mod:  26,
			c:    []int{15, 14, 7},
			key: [][]int{
				{6, 24, 1},
				{13, 16, 10},
				{20, 17, 15},
			},
			p: []int{0, 2, 19},
		},
		{
			name: "Wikipedia 2",
			mod:  26,
			c:    []int{5, 8, 13},
			key: [][]int{
				{6, 24, 1},
				{13, 16, 10},
				{20, 17, 15},
			},
			p: []int{2, 0, 19},
		},
		{
			name: "Wikipedia 3",
			mod:  26,
			c:    []int{7, 8},
			key: [][]int{
				{3, 3},
				{2, 5},
			},
			p: []int{7, 4},
		},
		{
			name: "Wikipedia 4",
			mod:  26,
			c:    []int{0, 19},
			key: [][]int{
				{3, 3},
				{2, 5},
			},
			p: []int{11, 15},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Decrypt(tt.c, tt.key, tt.mod)
			if err != nil {
				t.Errorf("Decrypt() got err: %v", err)
			}
			if diff := cmp.Diff(tt.p, got); diff != "" {
				t.Errorf("Decrypt() mismatch (-want +got):\n%s", diff)
			}
		})
	}
}

func TestInvert(t *testing.T) {
	tests := []struct {
		name string
		mod  int
		key  [][]int
		want [][]int
	}{
		{
			name: "Wikipedia 1",
			mod:  26,
			key: [][]int{
				{6, 24, 1},
				{13, 16, 10},
				{20, 17, 15},
			},
			want: [][]int{
				{8, 5, 10},
				{21, 8, 21},
				{21, 12, 8},
			},
		},
		{
			name: "Wikipedia 2",
			mod:  26,
			key: [][]int{
				{3, 3},
				{2, 5},
			},
			want: [][]int{
				{15, 17},
				{20, 9},
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := InvertMatrix(tt.key, tt.mod)
			if err != nil {
				t.Errorf("InvertMatrix() got err: %v", err)
			}
			if diff := cmp.Diff(tt.want, got); diff != "" {
				t.Errorf("InvertMatrix() mismatch (-want +got):\n%s", diff)
			}
		})
	}
}

func TestUnit(t *testing.T) {
	want := [][]int{{1, 0, 0, 0, 0}, {0, 1, 0, 0, 0}, {0, 0, 1, 0, 0}, {0, 0, 0, 1, 0}, {0, 0, 0, 0, 1}}
	m := unit(5)
	if diff := cmp.Diff(want, m); diff != "" {
		t.Errorf("unit() mismatch (-want +got):\n%s", diff)
	}
}

func TestEgcd(t *testing.T) {
	if g, x, y := egcd(240, 46); g != 2 && x != -9 && y != 47 {
		t.Errorf("egcd() got: %d, %d, %d want: 2, -9, 47", g, x, y)
	}
}

func TestModinv(t *testing.T) {
	got, err := modinv(2, 15)
	if err != nil {
		t.Errorf("modinv(2, 15) got err: %v", err)
	}
	if got != 8 {
		t.Errorf("modinv(2, 15) got: %d want: 8", got)
	}
}

func TestModinvInvalid(t *testing.T) {
	_, err := modinv(3, 15)
	if err == nil {
		t.Error("modinv(3, 15) got: nil want: error")
	}
}
