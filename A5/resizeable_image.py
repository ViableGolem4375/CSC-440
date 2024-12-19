
import imagematrix
import operator

class ResizeableImage(imagematrix.ImageMatrix):

    """
    This function returns a list of coordinates which correspond to the
    lowest energy vertical seam. It also allows the user to choose between
    using the naive algorithm to compute this seam, or the dynamic programming
    algorithm to compute the seam.
    """
    def best_seam(self, dp=True):
        self.energy_list = {}
        for x in range(self.width):
            for y in range(self.height):
                self.energy_list[x, y] = self.energy(x, y)
        if dp:
            return self.dynamic_best_seam(self.energy_list)
        else:
            return self.naive_best_seam(self.energy_list)

    """
    Given function to remove the seam from the given image.
    """
    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

    """
    Dynamic programming version of the seam carving algorithm. Works by
    creating a memoized list which is updated as the algorithm runs, this
    list is then used to make decisions on which pixel to add to the seam.
    The function then returns the computed seam as a list of coordinates.
    """
    def dynamic_best_seam(self, energy_list):
        # Lists to store the results of computations. Both a temporary
        # and memoized version.
        self.temp = {}
        self.memoized = {}

        for x in range(self.width):
            self.memoized[x, 0] = self.energy_list[x, 0]
            self.temp[x, 0] = [(x, 0)]

        row_minimum = []
        for y in range(1, self.height):
            for x in range(self.width):
                min_list = []
                min_list_path = {}
                left_pixel = (x - 1, y - 1)
                middle_pixel = (x, y - 1)
                right_pixel = (x + 1, y - 1)

                # If statement to decide which pixel to choose.
                if(x == 0):
                    options = [middle_pixel, right_pixel]
                elif(x == self.width - 1):
                    options = [left_pixel, middle_pixel]
                else:
                    options = [left_pixel, middle_pixel, right_pixel]

                for option in options:
                    min_list.append(self.memoized[option])
                    min_list_path[self.memoized[option]] = option
                
                min_energy = min(min_list)

                self.memoized[x, y] = min_energy + self.energy_list[x, y]

                for lowest in min_list:
                    if(lowest == min_energy):
                        self.temp[x, y] = self.temp[min_list_path[lowest]] + [(x, y)]

                if(y == self.height - 1):
                    if(x == 0):
                        row_minimum.append(self.memoized[x, y])
                        row_minimum.append((x, y))
                        row_minimum.append(min(min_list))
                        row_minimum.append(min_list_path[self.memoized[option]])
                    else:
                        if(row_minimum[0]>self.memoized[x, y]):
                            row_minimum[0] = self.memoized[x, y] 
                            row_minimum[1] = (x, y)
                            row_minimum[2] = min(min_list)
                            row_minimum[3] = min_list_path[self.memoized[option]]

        return self.temp[row_minimum[3]] + [row_minimum[1]]
  
    """
    Naive version of the seam carving algorithm, works by just recursively
    finding all of the possible seam locations in a given image, and then 
    choosing the best one from the options.
    """
    def naive_best_seam(self, energy_list):
        seam_list = []
        for x in range(self.width - 1):
            seam_list = self.recursive_best_seam(x, 0)
        print(seam_list)
        return seam_list


    """ 
    Function that recursively finds the best seam in a given list of pixels
    and returns a list of tuples with pixel coordinates.
    """
    def recursive_best_seam(self, x, y):
        # if statement which does the recursive function calls to find the
        # best seam.
        if(y == self.height - 1):
            return [(x, y)]
        else:
            if(x == 0):
                middle_pixel = self.recursive_best_seam(x, y + 1)
                right_pixel = self.recursive_best_seam(x + 1, y + 1)
                seams = [middle_pixel, right_pixel]
                seam_energies = [self.compute_seam_energy(middle_pixel), \
                                self.compute_seam_energy(right_pixel)]

            elif(x == self.width - 1):
                left_pixel = self.recursive_best_seam(x - 1, y + 1)
                middle_pixel = self.recursive_best_seam(x, y + 1)
                seams = [left_pixel, middle_pixel]
                seam_energies = [self.compute_seam_energy(left_pixel), \
                                self.compute_seam_energy(middle_pixel)]

            else:
                left_pixel = self.recursive_best_seam(x - 1, y + 1)
                middle = self.recursive_best_seam(x, y + 1)
                right_pixel = self.recursive_best_seam(x + 1, y + 1)
                seams = [left_pixel, middle, right_pixel]
                seam_energies = [self.compute_seam_energy(left_pixel), \
                                self.compute_seam_energy(middle), \
                                self.compute_seam_energy(right_pixel)]

            best_seam_index = seam_energies.index(min(seam_energies))
            best_seam_here = seams[best_seam_index]

            return [(x, y)] + best_seam_here

    """
    Function to compute the total energy of a computed seam.
    """
    def compute_seam_energy(self, seam):
        total_energy = 0
        for pixel in seam:
            total_energy += self.energy_list[pixel]
        return total_energy
