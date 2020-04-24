'''
Algo-
Makes a decision tree with go down or go right
solves number of turns for each (by collision)
pics one with lesser number of turns

'''

'''
Proposed algo-
At each pixel, check distance of obstacle to right & front,
take 1 step in the direction of longer collision.
'''

def get_dist(curr_pixel,maze):
	try:
		col=maze[:curr_pixel[0],curr_pixel[1]]
		y_dist=0
		for y in range(len(col),0,-1):
			if col[y]==1:
				break
			else:
				y_dist+=1			#can be done by DP too...
	except:
		y_dist=-100000000000

	try:

		row=maze[curr_pixel[0],curr_pixel[1]:]
		x_dist=0
		for i in range(0,len(row)):
			if row[i]==1:
				break
			else:
				x_dist+=1
	except:
		x_dist=-10000000000

	if x_dist<=1 and y_dist<=1:
		print(str(curr_pixel)+' Path terminated')
		raise ValueError('Path does not exist')
	if(x_dist>y_dist):
		return 1
	elif(y_dist>x_dist):
		return 0
	else:
		return -1


def get_path(maze):				#maze is a 2-d array of 0s and 1s, top left is origin, bottom right is target
	default=maze.shape.index(max(maze.shape))		#tells whether default turn is right or down
	maze=np.c_[np.ones((maze.shape[0],1)),maze,np.ones((maze.shape[0],1))]
	maze=np.r_[np.ones((1,maze.shape[1])),maze,np.ones((1,maze.shape[1]))]		#padding
	path=[]
	curr_pixel=[1,maze.shape[1]-2]
	dict={0:'r',1:'u'}
	#maze[1][2]=1
	i=0
	while curr_pixel!=[maze.shape[0]-2,1] and i<15000:
		
		try:
			choice=get_dist(curr_pixel,maze)
			if(choice == 0):

				curr_pixel[choice]+=1
				path.append(dict[choice])
			elif choice == 1:
				curr_pixel[choice]-=1
				path.append(dict[choice])
			else:
				curr_pixel[default]+=1
				path.append(dict[default])
		except:
			break
			#return([])
		maze[curr_pixel[0]][curr_pixel[1]]=-1
		i+=1
    

	#print(maze)
	path.append('p')
	rev_path=[]
	for dir in path:
		if dir == 'r':
			rev_path.append('l')
		elif dir == 'u':
			rev_path.append('d')
	path=path+reverse(rev_path)
	path.append('x')
	print(i)
	return path


'''
A* Approach
'''
'''
def manhattan_dist(point1,point2):
	return(abs(point2[0]-point1[0])+abs(point2[1]-point1[1]))

def key(point):
	return point[0]

def find_matrix(src,dest,maze):
	X=maze.shape[0]
	Y=maze.shape[1]
	
	cell_details=np.zeros((maze.shape[0],maze.shape[1],5))		#contains parent_x,parent_y,f,g,h
	closed_list=np.zeros((maze.shape[0],maze.shape[1]))

	for i in range(0,maze.shape[0]):
		for j in range(0,maze.shape[1]):
			cell_details[i][j][0]=-1
			cell_details[i][j][1]=-1
			cell_details[i][j][2]=100000000000000
			cell_details[i][j][3]=100000000000000
			cell_details[i][j][4]=100000000000000

	i=src[0]			
	j=src[1]

	cell_details[i][j][0]=i
	cell_details[i][j][1]=j
	cell_details[i][j][2]=0.0
	cell_details[i][j][3]=0.0
	cell_details[i][j][4]=0.0
	
	open_list=[]

	element=(0.0,src)
	open_list.append(element)

	foundDest=False

	while(len(open_list)):
		open_list.sort(key=key)
		curr_point=open_list.pop()
		i=curr_point[1][0]
		j=curr_point[1][0]
		closed_list[i][j]=1

		if ((i-1) in range(0,X)) and (j in range(0,Y)):
			if i-1==dest[0] and j==dest[1]:
				cell_details[i-1][j][0]=i
				cell_details[i-1][j][1]=j
				foundDest=True
				return cell_details
			elif(closed_list[i-1][j]==False and maze[i-1][j]==0):
				g_new=cell_details[i][j][3]+1.0
				h_new=manhattan_dist([i-1,j],dest)
				f_new=g_new+h_new

				if(cell_details[i-1][j]>f_new):
					element=(f_new,[i-1,j])
					open_list.append(element)

					cell_details[i-1][j][0]=i
					cell_details[i-1][j][1]=j
					cell_details[i-1][j][2]=f_new
					cell_details[i-1][j][3]=g_new
					cell_details[i-1][j][4]=h_new

		if ((i) in range(0,X)) and ((j-1) in range(0,Y)):
			if i==dest[0] and j-1==dest[1]:
				cell_details[i][j-1][0]=i
				cell_details[i][j-1][1]=j
				foundDest=True
				return cell_details
			elif(closed_list[i][j-1]==False and maze[i][j-1]==0):
				g_new=cell_details[i][j][3]+1.0
				h_new=manhattan_dist([i,j-1],dest)
				f_new=g_new+h_new

				if(cell_details[i][j-1]>f_new):
					element=(f_new,[i,j-1])
					open_list.append(element)

					cell_details[i][j-1][0]=i
					cell_details[i][j-1][1]=j
					cell_details[i][j-1][2]=f_new
					cell_details[i][j-1][3]=g_new
					cell_details[i][j-1][4]=h_new
		
		if ((i+1) in range(0,X)) and (j in range(0,Y)):
			if i+1==dest[0] and j==dest[1]:
				cell_details[i+1][j][0]=i
				cell_details[i+1][j][1]=j
				foundDest=True
				return cell_details
			elif(closed_list[i+1][j]==False and maze[i+1][j]==0):
				g_new=cell_details[i][j][3]+1.0
				h_new=manhattan_dist([i+1,j],dest)
				f_new=g_new+h_new

				if(cell_details[i+1][j]>f_new):
					element=(f_new,[i+1,j])
					open_list.append(element)

					cell_details[i+1][j][0]=i
					cell_details[i+1][j][1]=j
					cell_details[i+1][j][2]=f_new
					cell_details[i+1][j][3]=g_new
					cell_details[i+1][j][4]=h_new
		
		if ((i) in range(0,X)) and (j+1 in range(0,Y)):
			if i==dest[0] and j+1==dest[1]:
				cell_details[i][j+1][0]=i
				cell_details[i][j+1][1]=j
				foundDest=True
				return cell_details
			elif(closed_list[i][j+1]==False and maze[i][j+1]==0):
				g_new=cell_details[i][j][3]+1.0
				h_new=manhattan_dist([i,j+1],dest)
				f_new=g_new+h_new

				if(cell_details[i][j+1]>f_new):
					element=(f_new,[i,j+1])
					open_list.append(element)

					cell_details[i][j+1][0]=i
					cell_details[i][j+1][1]=j
					cell_details[i][j+1][2]=f_new
					cell_details[i][j+1][3]=g_new
					cell_details[i][j+1][4]=h_new

	if foundDest==False:
		raise ValueError('No Path found')
'''
# from PIL import Image
# import numpy as np

# maze=np.array(Image.open('mask.jpg'))
# maze=(maze[:,:]/240).astype(int)
# '''
# maze=maze*255
# maze=abs(maze)
# res=Image.fromarray(maze.astype(np.uint8))
# res.save('final.jpg')
# '''

# mat=find_matrix([0,0],[3023,4031],maze)










