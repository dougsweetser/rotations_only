# Rotations Only, the Webapp

This is a webapp to explore rotation functions. The need for this webapp arose from a disagreement. Everyone knows that quaternions
are fine for doing rotations in 3D space using a quaternion triple product. This was first done in 1843 by Rodrigues:

$$ R \rightarrow R' = U R U^{-1} $$

After Einstein developed special relativity, it was his math professor Minkowski who saw that special relativity was just a
rotation in 4D space-time. It was an obvious to look for a way to generalize this triple product to do such a transformation.
If one uses this exact function, real-valued quaternions are not up to the task. Conway and Silberstein in 1911-1912 showed
that if one uses complex-valued quaternions which are not a division algebra, then Lorentz boosts could be done with the
Rodrigues formula.

A century later, I reconsidered this problem. What if more terms were added?

$$ R \rightarrow R' = U R U^*  + \frac{1}{2}( (U U R)^* - (U^* U^* R)^*) $$

A direct calculation shows this does the Lorentz boost one needs to do the work of special relativity. This expression was
discovered independently by Dr. Kharinov. My name for this function is the Generalized Rodrigues function.

I then hit an unexpected roadblock. Both Dr. Kharinov and a fellow who writes to me under the name Purple Penguin do not
believe this function for boosts can also do 3D rotations!

This streamlit webapp was designed to show the rotations that are obviously possible with the Rodrigues function can also be 
done with the Generalized Rodrigues function
