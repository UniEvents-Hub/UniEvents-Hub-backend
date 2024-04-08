import numpy as np
import matplotlib
import matplotlib.image as image


def read_as_compressed(U, S, VT, k):
        A = np.zeros((U.shape[0], VT.shape[1]))
        for i in range(k):
            U_i = U[:,[i]]
            VT_i = np.array([VT[i]])
            A += S[i] * (U_i @ VT_i)
        return A
def svdCompression(imagepath,compression_rate):
    imagepath = f"../mediafiles/{imagepath}"
    A = image.imread("rendered_image.png")
    R = A[:,:,0] / 0xff
    G = A[:,:,1] / 0xff
    B = A[:,:,2] / 0xff

    R_U, R_S, R_VT = np.linalg.svd(R)
    G_U, G_S, G_VT = np.linalg.svd(G)
    B_U, B_S, B_VT = np.linalg.svd(B)

    relative_rank = 0.1
    max_rank = int(relative_rank * min(R.shape[0], R.shape[1]))
    k = 10
    rank = int((k/100)*max_rank)


    R_compressed = read_as_compressed(R_U, R_S, R_VT, rank)
    G_compressed = read_as_compressed(G_U, G_S, G_VT, rank)
    B_compressed = read_as_compressed(B_U, B_S, B_VT, rank)

    compressed_float = np.dstack((R_compressed, G_compressed, B_compressed))
    compressed = (np.minimum(compressed_float, 1.0) * 0xff).astype(np.uint8)
    
    return compressed