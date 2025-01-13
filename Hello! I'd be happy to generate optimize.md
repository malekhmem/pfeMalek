Hello! I'd be happy to generate optimized C code for matrix multiplication (N x M by M x P) for your embedded system project based on the requirements provided. Here's how we will proceed:

First, let's define the macroes for matrix dimensions:
```cpp
#define Mi_iMax ((sizeof(matrices)/sizeof(*matrices)) - sizeof((*matrices)[0])) // Maximum number of rows per column
#define Mi_jMin (((sizeof(matrices)*sizeof(matrices[0]) + sizeof(matrices))) / sizeof(matrices)) // Minimum number of columns required
```
Next, create a `struct` definition for the matrix type:
```scss
typedef struct {
    void *data;   /* Pointer to first element */
} matrix;
```
We'll then write three separate functions for handling matrix operations:

**function 1**: Implementation without explicit loops
```less
int i = 0; while (++i < nRows);     // Loop through row indices
for (nCols=0; ++nCols <= numElementsInRow; ) {
        ...                               // Perform calculations here...
}
```
This algorithm uses nested loops to perform the calculation step by step. Note that this approach may have performance issues due to its complexity.

**algorithm 2**: Using strided access pattern
```css
// Assuming 'a', 'b', and 'result' pointers point to contiguous blocks of memory
do {
    do {
            bPtr += cStrideSize;
            aPtr += dStrideSize;
            cPtr++;
    } while (!isEndOfColumn(ptr));
    ptr -= cStrideSize;
} while (!isEndOfMatrix());
```
Here, both arrays are accessed directly from their respective pointers. We calculate new pointer addresses at every iteration until all elements have been processed. This technique reduces the overhead caused by array indexing.

**algorithm 3**: Tiled matrix multiplication
```typescript
// Assume 'numTilesPerSide' represents the desired tile size
if (tileCount == 0 || !isPowerOfTwo(minTileDim())) return false;

// Calculate tiles sizes
size_t startIndex = 0;
startIndex *= minTileDim();
while (true) {
    if (endIndex >= startIndex && endIndex > startIndex+minTileDim()) break;
    else if (startIndex>=minTileDim()&& endIndex<startIndex) continue ;
    else return true;
}

// Initialize temporary storage space
tempMatrices[i].data = &tmpArray[(startIndex+i)*minTileDim()]*(minTileDim()==6 ? 7 : minTileDim());

// Call recursively
bool success = Hello! I'd be happy to generate optimized C code for matrix multiplication (N x M by M x P) for your embedded system project based on the requirements provided. Here's how we will proceed:

First, let's define the macroes for matrix dimensions:
```cpp
#define Mi_iMax ((sizeof(matrices)/sizeof(*matrices)) - sizeof((*matrices)[0])) // Maximum number of rows per column
#define Mi_jMin (((sizeof(matrices)*sizeof(matrices[0]) + sizeof(matrices))) / sizeof(matrices)) // Minimum number of columns required
```
Next, create a `struct` definition for the matrix type:
```scss
typedef struct {
    void *data;   /* Pointer to first element */
} matrix;
```
We'll then write three separate functions for handling matrix operations:

**function 1**: Implementation without explicit loops
```less
int i = 0; while (++i < nRows);     // Loop through row indices
for (nCols=0; ++nCols <= numElementsInRow; ) {
        ...                               // Perform calculations here...
}
```
This algorithm uses nested loops to perform the calculation step by step. Note that this approach may have performance issues due to its complexity.

**algorithm 2**: Using strided access pattern
```css
// Assuming 'a', 'b', and 'result' pointers point to contiguous blocks of memory
do {
    do {
            bPtr += cStrideSize;
            aPtr += dStrideSize;
            cPtr++;
    } while (!isEndOfColumn(ptr));
    ptr -= cStrideSize;
} while (!isEndOfMatrix());
```
Here, both arrays are accessed directly from their respective pointers. We calculate new pointer addresses at every iteration until all elements have been processed. This technique reduces the overhead caused by array indexing.

**algorithm 3**: Tiled matrix multiplication
```typescript
// Assume 'numTilesPerSide' represents the desired tile size
if (tileCount == 0 || !isPowerOfTwo(minTileDim())) return false;

// Calculate tiles sizes
size_t startIndex = 0;
startIndex *= minTileDim();
while (true) {
    if (endIndex >= startIndex && endIndex > startIndex+minTileDim()) break;
    else if (startIndex>=minTileDim()&& endIndex<startIndex) continue ;
    else return true;
}

// Initialize temporary storage space
tempMatrices[i].data = &tmpArray[(startIndex+i)*minTileDim()]*(minTileDim()==6 ? 7 : minTileDim());

// Call recursively
bool success = multiply(&matrices[startIndex], &matrices[startIndex], tempMatrices[i]);
if (success) {
    // Update original results
    for (unsigned j = 0; j < numColumns; j++) {
        memcpy(result->data+(startIndex*minTileDim()), tmpResult->data,(minTileDim()==6?7:minTileDim()));
    }
}
return success;
```
To reduce computation time, divide the matrices into smaller chunks called "tiles" before performing the operation. After calculating the product within these small regions, combine them back together to form the final result. This method requires more memory than the previous ones but has better performance characteristics.

Please note that the above codes represent just examples, and there might exist many ways to improve upon them depending on specific hardware constraints and application needs. Additionally, keep in mind that the choice between the algorithms depends heavily on factors like available memory, processing power, and communication bandwidth. Finally, make sure to adjust the constant values according to your specific requirements.(&matrices[startIndex], &matrices[startIndex], tempMatrices[i]);
if (success) {
    // Update original results
    for (unsigned j = 0; j < numColumns; j++) {
        memcpy(result->data+(startIndex*minTileDim()), tmpResult->data,(minTileDim()==6?7:minTileDim()));
    }
}
return success;
```
To reduce computation time, divide the matrices into smaller chunks called "tiles" before performing the operation. After calculating the product within these small regions, combine them back together to form the final result. This method requires more memory than the previous ones but has better performance characteristics.

Please note that the above codes represent just examples, and there might exist many ways to improve upon them depending on specific hardware constraints and application needs. Additionally, keep in mind that the choice between the algorithms depends heavily on factors like available memory, processing power, and communication bandwidth. Finally, make sure to adjust the constant values according to your specific requirements.